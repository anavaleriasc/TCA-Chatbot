"use client";

import { useState, useEffect } from "react";
import Sidebar from "@/components/Sidebar";
import ChatWindow from "@/components/ChatWindow";
import MessageInput from "@/components/MessageInput";

export interface MessageType {
  id: string;
  text: string;
  sender: "user" | "bot";
}

export interface SessionType {
  id: number;
  thread_id: string;
  conversation_summary?: string;
}

export default function ChatPage() {
  const [sessions, setSessions] = useState<SessionType[]>([]);
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [activeThreadId, setActiveThreadId] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const currentUserId = 1;

  useEffect(() => {
    fetchSessions();
    handleNewSession();
  }, []);

  const fetchSessions = async () => {
    try {
      const res = await fetch("http://52.67.190.156:8000/sessoes");
      if (res.ok) {
        const data = await res.json();
        setSessions(data);
      }
    } catch (error) {
      console.error("Erro ao buscar sessões", error);
    }
  };

  const fetchMessages = async (threadId: string) => {
    try {
      const res = await fetch(`http://52.67.190.156:8000/mensagens/${threadId}`);
      if (res.ok) {
        const data = await res.json();
        const formattedMessages: MessageType[] = data.map((msg: any, index: number) => ({
          id: msg.id ? msg.id.toString() : `fallback-id-${index}-${Date.now()}`,
          text: msg.content || "",
          sender: msg.role === "user" ? "user" : "bot"
        }));
        setMessages(formattedMessages);
      }
    } catch (error) {
      console.error("Erro ao buscar histórico", error);
    }
  };

  const handleNewSession = () => {
    setActiveThreadId(`sessao-${Date.now()}`);
    setMessages([]);
  };

  const handleSelectSession = (threadId: string) => {
    if (activeThreadId !== threadId) {
      setActiveThreadId(threadId);
      fetchMessages(threadId);
    }
  };

  // NOVA FUNÇÃO: Renomear Sessão
  const handleRenameSession = async (threadId: string, newName: string) => {
    if (!newName.trim()) return;

    // 1. Atualiza visualmente na mesma hora
    setSessions((prev) => 
      prev.map((s) => s.thread_id === threadId ? { ...s, conversation_summary: newName } : s)
    );

    // 2. Manda para o backend atualizar no banco de dados
    try {
      await fetch(`http://52.67.190.156:8000/sessoes/${threadId}`, {
        method: "PATCH", // Ou PUT, dependendo de como o backend estiver configurado
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ conversation_summary: newName })
      });
    } catch (error) {
      console.error("Erro ao renomear a sessão no backend", error);
    }
  };

  // NOVA FUNÇÃO: Excluir Sessão
  const handleDeleteSession = async (threadId: string) => {
    // 1. Remove da lista visualmente (o React já junta os botões de baixo automaticamente, sem deixar buraco)
    setSessions((prev) => prev.filter((s) => s.thread_id !== threadId));

    // 2. Se apagou a sessão que estava aberta, limpa a tela para uma nova
    if (activeThreadId === threadId) {
      handleNewSession();
    }

    // 3. Pede para o backend deletar do banco
    try {
      await fetch(`http://52.67.190.156:8000/sessoes/${threadId}`, {
        method: "DELETE",
      });
    } catch (error) {
      console.error("Erro ao excluir a sessão no backend", error);
    }
  };

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const isFirstMessage = messages.length === 0;

    const userMsg: MessageType = { id: Date.now().toString(), text, sender: "user" };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await fetch("http://52.67.190.156:8000/chat/invoke", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: currentUserId,
          thread_id: activeThreadId,
          message: text
        })
      });

      if (response.ok) {
        const data = await response.json();
        const botMsg: MessageType = {
          id: (Date.now() + 1).toString(),
          text: data.message || "Sem resposta do modelo.",
          sender: "bot"
        };
        setMessages((prev) => [...prev, botMsg]);

        if (isFirstMessage) {
          fetchSessions();
        }
      } else {
        console.error("Erro na API ao processar a mensagem.");
      }
    } catch (error) {
      console.error("Erro de conexão", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="app-container">
      <Sidebar 
        sessions={sessions} 
        activeThreadId={activeThreadId}
        onSelectSession={handleSelectSession}
        onNewSession={handleNewSession}
        onRenameSession={handleRenameSession}
        onDeleteSession={handleDeleteSession}
      />

      <section className="chat-container">
        <header className="chat-header">
          <div className="logo">
            <img src="/opala.png" alt="Opala Logo"/>
          </div>
        </header>

        <ChatWindow messages={messages} />

        <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </section>
    </main>
  );
}