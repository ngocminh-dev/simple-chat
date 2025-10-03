/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useRef, useState } from "react";
import type { Message } from "../types";

const API_BASE = (import.meta.env.VITE_API_BASE as string) || "http://localhost:8000";

function makeWsUrl(conversationId: number) {
  try {
    const u = new URL(API_BASE);
    const wsProto = u.protocol === "https:" ? "wss:" : "ws:";
    return `${wsProto}//${u.host}/chat/ws/${conversationId}`;
  } catch {
    const wsProto = window.location.protocol === "https:" ? "wss:" : "ws:";
    return `${wsProto}//${window.location.host}/chat/ws/${conversationId}`;
  }
}

export function useWebSocketChat(conversationId: number | null) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const pendingRef = useRef<string[]>([]); // queue messages if ws not open

  useEffect(() => {
    let aborted = false;

    async function fetchMessages() {
      if (!conversationId) {
        setMessages([]);
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE}/chat/conversations/${conversationId}/messages`);
        if (!res.ok) throw new Error(`Failed to load messages (${res.status})`);
        const data = (await res.json()) as Message[];
        if (!aborted) setMessages(data);
      } catch (err: any) {
        if (!aborted) setError(err.message || String(err));
      } finally {
        if (!aborted) setLoading(false);
      }
    }

    fetchMessages();

    // open websocket
    if (!conversationId) return () => { aborted = true; };

    const wsUrl = makeWsUrl(conversationId);
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      // flush pending
      while (pendingRef.current.length) {
        const p = pendingRef.current.shift()!;
        try {
          ws.send(JSON.stringify({ content: p }));
        } catch { /* empty */ }
      }
      console.log("[ws] open", wsUrl);
    };

    ws.onmessage = (evt) => {
      try {
        const incoming = JSON.parse(evt.data) as Message;
        setMessages((prev) => {
          // handle assistant streaming partial messages
          if (incoming.sender === "assistant" && incoming.partial) {
            // find last assistant partial
            const lastIdx = [...prev].map((m) => m.sender).lastIndexOf("assistant");
            if (lastIdx !== -1 && prev[lastIdx].partial) {
              const copy = [...prev];
              copy[lastIdx] = { ...copy[lastIdx], content: (copy[lastIdx].content || "") + incoming.content };
              return copy;
            }
            return [...prev, incoming];
          }
          // normal append
          return [...prev, incoming];
        });
      } catch (e) {
        console.warn("[ws] invalid message", e);
      }
    };

    ws.onclose = () => {
      console.log("[ws] closed");
      wsRef.current = null;
    };

    ws.onerror = (ev) => {
      console.error("[ws] error", ev);
    };

    return () => {
      aborted = true;
      try { ws.close(); } catch { /* empty */ }
      wsRef.current = null;
    };
  }, [conversationId]);

  const sendMessage = (content: string) => {
    if (!conversationId) return;
    const ws = wsRef.current;
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ content }));
    } else {
      // queue and ensure ws will open or reopen
      pendingRef.current.push(content);
      // if ws closed, try to create a temporary connection to flush
      if (!wsRef.current) {
        try {
          const wsTemp = new WebSocket(makeWsUrl(conversationId));
          wsRef.current = wsTemp;
          wsTemp.onopen = () => {
            while (pendingRef.current.length) {
              const p = pendingRef.current.shift()!;
              try { wsTemp.send(JSON.stringify({ content: p })); } catch {/* empty */ }
            }
          };
          wsTemp.onmessage = (evt) => {
            try {
              const incoming = JSON.parse(evt.data) as Message;
              setMessages((prev) => [...prev, incoming]);
            } catch {/* empty */ }
          };
          wsTemp.onclose = () => { wsRef.current = null; };
        } catch (e) {
          console.warn("[ws] cannot open", e);
        }
      }
    }
  };

  return { messages, sendMessage, loading, error };
}
