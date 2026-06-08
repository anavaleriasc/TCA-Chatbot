"use client";

import { useState, useEffect } from "react";
import Sidebar from "@/components/Sidebar";
import ChatWindow from "@/components/ChatWindow";
import MessageInput from "@/components/MessageInput";
import { useAuth } from "@/app/hooks/useAuth";

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

  const currentUserId = useAuth()?.auth?.user.id; // Pegando o ID do usuário logado do contexto

  useEffect(() => {
    fetchSessions();
    handleNewSession();
  }, []);

  const fetchSessions = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch("http://52.67.190.156:8000/sessoes", {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (res.ok) {
        const data = await res.json();
        setSessions(data);
      } else if (res.status === 401) {
        console.error("Token expirado ou inválido");
      }
    } catch (error) {
      console.error("Erro ao buscar sessões", error);
    }
  };

  const fetchMessages = async (threadId: string) => {
    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch(`http://52.67.190.156:8000/mensagens/${threadId}`, {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });
      if (res.ok) {
        const data = await res.json();
        const formattedMessages: MessageType[] = data.map((msg: any, index: number) => ({
          id: msg.id ? msg.id.toString() : `fallback-id-${index}-${Date.now()}`,
          text: msg.content || "",
          sender: msg.role === "user" ? "user" : "bot"
        }));
        setMessages(formattedMessages);
      } else if (res.status === 403) {
        console.error("Você não tem permissão para acessar este chat");
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
      const token = localStorage.getItem("access_token");
      await fetch(`http://52.67.190.156:8000/sessoes/${threadId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
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
      const token = localStorage.getItem("access_token");
      await fetch(`http://52.67.190.156:8000/sessoes/${threadId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`
        }
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
      const token = localStorage.getItem("access_token");
      const response = await fetch("http://52.67.190.156:8000/chat/invoke", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
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
      } else if (response.status === 401) {
        console.error("Token expirado. Por favor, faça login novamente.");
      } else if (response.status === 403) {
        console.error("Você não tem permissão para enviar mensagens como este usuário.");
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