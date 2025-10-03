import { useEffect, useState, type JSX } from "react";
import ChatWindow from "./components/ChatWindow";
import Sidebar from "./components/Sidebar";
import { useWebSocketChat } from "./hooks/useWebSocketChat";
import type { Conversation } from "./types";

const API_BASE = (import.meta.env.VITE_API_BASE as string) || "http://localhost:8000";

export default function App(): JSX.Element {
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [selectedConvId, setSelectedConvId] = useState<number | null>(null);
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

    const { messages, sendMessage, loading } = useWebSocketChat(selectedConvId);

    useEffect(() => {
        loadConversations();
    }, []);

    async function loadConversations() {
        try {
            const res = await fetch(`${API_BASE}/chat/conversations`);
            const data = await res.json();
            data.sort((a: Conversation, b: Conversation) => {
                if (a.created_at && b.created_at) return +new Date(b.created_at) - +new Date(a.created_at);
                return b.id - a.id;
            });
            setConversations(data);
        } catch (e) {
            console.error("Failed to load conversations", e);
        }
    }

    async function createConversation() {
        try {
            const res = await fetch(`${API_BASE}/chat/conversations`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: "New conversation" }),
            });
            const convo = await res.json();
            setConversations((prev) => [convo, ...prev]);
            setSelectedConvId(convo.id);
        } catch (e) {
            console.error("Failed to create conversation", e);
        }
    }
    function selectConversation(id: number) {
        setSelectedConvId(id);
        setConversations((prev) => {
            const idx = prev.findIndex((c) => c.id === id);
            if (idx === -1) return prev;
            const conv = prev[idx];
            const rest = prev.filter((c) => c.id !== id);
            return [conv, ...rest];
        });
    }

    return (
        <div className="h-screen flex flex-col">
            <div className="flex flex-1 overflow-hidden">

                <Sidebar
                    conversations={conversations}
                    onNewConversation={createConversation}
                    onSelectConversation={selectConversation}
                    collapsed={sidebarCollapsed}
                    setCollapsed={setSidebarCollapsed}
                    selectedId={selectedConvId}
                />


                <main className="flex-1 bg-slate-50 flex flex-col min-h-0">
                    <div className="flex-1 min-h-0">

                        <ChatWindow messages={messages} sendMessage={sendMessage} loading={loading} conversationId={selectedConvId}/>
                    </div>
                </main>
            </div>
        </div>
    );
}
