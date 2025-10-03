import React, { useEffect, useRef } from "react";
import type { Message } from "../types";
import Header from "./Header";
import MessageBubble from "./MessageBubble";

interface ChatWindowProps {
  conversationId: number | null;
  messages: Message[];
  sendMessage: (content: string) => void;
  loading: boolean;
}

const ChatWindow: React.FC<ChatWindowProps> = ({
  conversationId,
  messages,
  sendMessage,
  loading,
}) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleSend = () => {
    if (inputRef.current && inputRef.current.value.trim()) {
      sendMessage(inputRef.current.value);
      inputRef.current.value = "";
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);
  return (
    <div className="flex flex-col flex-1 h-screen">
      <Header title={conversationId ? `Conversation ${conversationId}` : "No Conversation"} />

      <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-white">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        {loading && (
          <div className="text-gray-400 italic">History chat is loading...</div>
        )}
        <div ref={messagesEndRef} />
      </div>
        {conversationId != null &&
      <div className="p-3 border-t bg-gray-50 flex items-center">
        <input
          ref={inputRef}
          type="text"
          placeholder="Type a message..."
          className="flex-1 px-3 py-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-500"
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button
          onClick={handleSend}
          className="ml-2 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
        >
          Send
        </button>
      </div>}
    </div>
  );
};

export default ChatWindow;
