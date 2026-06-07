"use client";

import MessageBubble from "./MessageBubble";
import { MessageType } from "@/app/chat/page"; // Ajuste o caminho se a sua ChatPage estiver em outra pasta

interface Props {
  messages: MessageType[];
}

export default function ChatWindow({ messages }: Props) {
  return (
    <div className="chat-window">
      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          sender={message.sender}
          text={message.text}
        />
      ))}
    </div>
  );
}