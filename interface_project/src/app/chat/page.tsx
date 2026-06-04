import Sidebar from "@/components/Sidebar";
import ChatWindow from "@/components/ChatWindow";
import MessageInput from "@/components/MessageInput";

export default function ChatPage() {
  return (
    <main className="app-container">

      <Sidebar />

      <section className="chat-container">

        <header className="chat-header">
          <h1 className="chat-title">
            OPALA
          </h1>
        </header>

        <ChatWindow />

        <MessageInput />

      </section>

    </main>
  );
}