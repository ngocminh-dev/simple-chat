import { useEffect, useRef, useState } from "react";
import ChatWindow from "./components/ChatWindow";
import InputBox from "./components/InputBox";
import TypingIndicator from "./components/TypingIndicator";
import "./styles/App.css";
import type { Message } from "./types/message";

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isBotTyping, setIsBotTyping] = useState(false);

  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const clientId = "frontend-" + Math.random().toString(36).slice(2, 9);
    const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
    wsRef.current = ws;

    ws.onopen = () => console.log("✅ WebSocket connected");

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === "partial") {
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last && last.sender === "bot") {
              const updated = { ...last, text: last.text + (data.delta ?? "") };
              return [...prev.slice(0, -1), updated];
            } else {
              return [...prev, { id: Date.now(), sender: "bot", text: data.delta ?? "" }];
            }
          });
          setIsBotTyping(false);
        }

        if (data.type === "end") {
          setIsBotTyping(false);
        }

        if (data.type === "response") {
          setMessages((prev) => [
            ...prev,
            { id: Date.now(), sender: "bot", text: data.message ?? "" },
          ]);
          setIsBotTyping(false);
        }
      } catch (err) {
        console.error("❌ Failed to parse WS message", err);
      }
    };

    ws.onclose = () => console.log("❌ WebSocket closed");
    ws.onerror = (err) => console.error("WebSocket error", err);

    return () => {
      ws.close();
    };
  }, []);

  const handleSend = (text: string) => {
    if (!text.trim()) return;
    const userMsg: Message = { id: Date.now(), sender: "user", text };
    setMessages((prev) => [...prev, userMsg]);
    wsRef.current?.send(JSON.stringify({ type: "message", message: text }));
    setIsBotTyping(true);
  };

  return (
    <div className="app-container dark">
      <div className="chat-area">
        <ChatWindow messages={messages} />
        {isBotTyping && <TypingIndicator />}
        <InputBox onSend={handleSend} />
      </div>
    </div>
  );
}
