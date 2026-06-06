"use client";

import { useState, useRef, useEffect } from "react";
import { SessionType } from "@/app/chat/page";

interface Props {
  sessions: SessionType[];
  activeThreadId: string;
  onSelectSession: (threadId: string) => void;
  onNewSession: () => void;
  onRenameSession: (threadId: string, newName: string) => void;
  onDeleteSession: (threadId: string) => void;
}

export default function Sidebar({
  sessions,
  activeThreadId,
  onSelectSession,
  onNewSession,
  onRenameSession,
  onDeleteSession
}: Props) {
  const [menuOpenId, setMenuOpenId] = useState<string | null>(null);
  const [renamingId, setRenamingId] = useState<string | null>(null);
  const [editName, setEditName] = useState("");
  const sidebarRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const handleClickOutside = () => {
      setMenuOpenId(null);
    };
    document.addEventListener("click", handleClickOutside);
    return () => document.removeEventListener("click", handleClickOutside);
  }, []);

  const startRename = (threadId: string, currentName: string) => {
    setRenamingId(threadId);
    setEditName(currentName);
    setMenuOpenId(null);
  };

  const finishRename = (threadId: string) => {
    onRenameSession(threadId, editName);
    setRenamingId(null);
  };

  return (
    <aside className="sidebar" ref={sidebarRef}>
      <div className="sidebar-header">
        <h2 className="sidebar-title">Conversas</h2>
      </div>

      <button className="new-chat-btn" onClick={onNewSession}>
        Nova Conversa
      </button>

      <div className="sessions-list" style={{ overflowY: "auto", overflowX: "visible" }}>
        {sessions.map((session) => {
          const sessionName = session.conversation_summary || session.thread_id;
          const isActive = activeThreadId === session.thread_id;
          const isRenaming = renamingId === session.thread_id;
          const isMenuOpen = menuOpenId === session.thread_id;

          return (
            <div
              key={session.thread_id}
              className={`session-card ${isActive ? "active" : ""}`}
              onClick={() => {
                if (!isRenaming) onSelectSession(session.thread_id);
              }}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                padding: "12px 20px", // Ajustado para dar mais "ar" nas laterais
                cursor: "pointer",
                backgroundColor: isActive ? "#374151" : "transparent",
                border: isActive ? "1px solid #4b5563" : "1px solid transparent",
                borderRadius: "32px", // <--- DEIXA O BOTÃO ARREDONDADO (ESTILO PÍLULA)
                marginBottom: "10px",
                transition: "all 0.2s ease-in-out",
                position: "relative",
              }}
            >
              
              {/* 1. ÁREA DO TÍTULO */}
              <div style={{ flex: 1, overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis", marginRight: "10px" }}>
                {isRenaming ? (
                  <input
                    autoFocus
                    value={editName}
                    onChange={(e) => setEditName(e.target.value)}
                    onBlur={() => finishRename(session.thread_id)}
                    onClick={(e) => {
                      e.stopPropagation();
                      e.nativeEvent.stopImmediatePropagation();
                    }}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") {
                        e.stopPropagation();
                        finishRename(session.thread_id);
                      }
                    }}
                    style={{
                      width: "100%",
                      background: "transparent",
                      border: "1px solid #6b7280",
                      color: "#fff",
                      padding: "2px 8px",
                      borderRadius: "16px", // Input também ligeiramente arredondado
                      outline: "none",
                    }}
                  />
                ) : (
                  <span style={{ color: "#d1d5db", fontSize: "15px", fontWeight: isActive ? "500" : "400" }}>
                    {sessionName}
                  </span>
                )}
              </div>

              {/* 2. ÁREA DO BOTÃO 3 PONTOS E MENU */}
              <div style={{ position: "relative" }}>
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation(); 
                    e.nativeEvent.stopImmediatePropagation(); 
                    
                    setMenuOpenId((prev) => (prev === session.thread_id ? null : session.thread_id));
                    setRenamingId(null);
                  }}
                  style={{
                    background: "none",
                    border: "none",
                    color: "#9ca3af",
                    cursor: "pointer",
                    padding: "4px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    borderRadius: "50%", // Deixa o hover/fundo do botão dos 3 pontinhos redondo também
                    width: "28px",
                    height: "28px",
                  }}
                  onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "rgba(255,255,255,0.1)")}
                  onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
                >
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                    <circle cx="8" cy="3" r="1.5" />
                    <circle cx="8" cy="8" r="1.5" />
                    <circle cx="8" cy="13" r="1.5" />
                  </svg>
                </button>

                {/* Dropdown Menu */}
                {isMenuOpen && (
                  <div
                    style={{
                      position: "absolute",
                      top: "100%",
                      right: "0",
                      marginTop: "8px",
                      backgroundColor: "#1f2937",
                      border: "1px solid #374151",
                      borderRadius: "12px", // Menus dropdown com bordas mais suaves
                      boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.3)",
                      zIndex: 9999,
                      display: "flex",
                      flexDirection: "column",
                      overflow: "hidden",
                      minWidth: "130px",
                      padding: "4px 0"
                    }}
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      e.nativeEvent.stopImmediatePropagation(); 
                    }} 
                  >
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        e.nativeEvent.stopImmediatePropagation();
                        startRename(session.thread_id, sessionName);
                      }}
                      style={{ padding: "10px 16px", color: "#e5e7eb", background: "none", border: "none", cursor: "pointer", textAlign: "left", fontSize: "14px", transition: "background-color 0.2s" }}
                      onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#374151")}
                      onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
                    >
                      Renomear
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        e.nativeEvent.stopImmediatePropagation();
                        onDeleteSession(session.thread_id);
                        setMenuOpenId(null);
                      }}
                      style={{ padding: "10px 16px", color: "#ef4444", background: "none", border: "none", cursor: "pointer", textAlign: "left", fontSize: "14px", transition: "background-color 0.2s" }}
                      onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#374151")}
                      onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
                    >
                      Excluir
                    </button>
                  </div>
                )}
              </div>

            </div>
          );
        })}
      </div>
    </aside>
  );
}