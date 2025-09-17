import { useState } from "react";

interface InputBoxProps {
  onSend: (text: string) => void;
}

export default function InputBox({ onSend }: InputBoxProps) {
  const [text, setText] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  return (
    <form className="input-box" onSubmit={handleSubmit}>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Ask anything"
      />
      <button type="submit">Send</button>
    </form>
  );
}
