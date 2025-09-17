
import type { Message } from "../types/message";
import MessageItem from "./Message";

interface ChatWindowProps {
  messages: Message[];
}

export default function ChatWindow({ messages }: ChatWindowProps) {
  return (
    <div className="chat-window">
      {messages.map((msg) => (
        <MessageItem key={msg.id} sender={msg.sender} text={msg.text} />
      ))}
    </div>
  );
}
