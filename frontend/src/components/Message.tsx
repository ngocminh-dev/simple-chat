import { useEffect, useState } from "react";

interface MessageProps {
  sender: "user" | "bot";
  text: string;
}

export default function MessageItem({ sender, text }: MessageProps) {
  const isUser = sender === "user";
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const timeout = setTimeout(() => setVisible(true), 50);
    return () => clearTimeout(timeout);
  }, []);

  return (
    <div className={`message-row ${isUser ? "user" : "bot"} ${visible ? "show" : ""}`}>
      <div className={`message-bubble ${isUser ? "user-bubble" : "bot-bubble"}`}>
        {text}
      </div>
    </div>
  );
}
