"use client";

import { useState, useRef } from "react";

interface Props {
  onSendMessage: (text: string) => void;
  isLoading: boolean;
}

export default function MessageInput({ onSendMessage, isLoading }: Props) {
  const [message, setMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  };

  const handleSend = () => {
    if (message.trim() !== "" && !isLoading) {
      onSendMessage(message);
      setMessage("");
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div style={{ padding: "20px", display: "flex", justifyContent: "center", width: "100%" }}>
      <div style={{
        display: "flex",
        alignItems: "flex-end",
        width: "100%",
        maxWidth: "800px",
        backgroundColor: "#1e1f20", 
        borderRadius: "32px",
        padding: "12px 24px",
        border: "1px solid #374151",
        transition: "border-radius 0.2s ease",
        opacity: isLoading ? 0.6 : 1 // Dá um efeito visual escurecido enquanto carrega
      }}>
        
        <textarea
          ref={textareaRef}
          value={message}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          placeholder="Converse com Opala..."
          rows={1}
          style={{
            flex: 1,
            backgroundColor: "transparent",
            border: "none",
            outline: "none",
            color: "#e5e7eb",
            fontSize: "16px",
            lineHeight: "24px",
            fontFamily: "inherit",
            resize: "none",
            padding: "0",
            margin: "0",
            minHeight: "24px",
            maxHeight: "144px",
            overflowY: "auto",
            scrollbarWidth: "thin",
          }}
        />

        <button 
          onClick={handleSend}
          disabled={isLoading}
          style={{
            marginLeft: "16px",
            marginBottom: "2px",
            backgroundColor: "transparent",
            border: "none",
            color: isLoading ? "#4b5563" : "#9ca3af",
            fontWeight: "600",
            fontSize: "16px",
            cursor: isLoading ? "not-allowed" : "pointer",
            outline: "none"
        }}>
          {isLoading ? "..." : "Enviar"}
        </button>
      </div>
    </div>
  );
}