import { mockSessions } from "@/data/mock";
import MessageBubble from "./MessageBubble";

export default function ChatWindow() {

  const session = mockSessions[0];

  return (
    <div className="chat-window">

      {session.messages.map((message) => (
        <MessageBubble
          key={message.id}
          sender={message.sender}
          text={message.text}
        />
      ))}

    </div>
  );
  
}