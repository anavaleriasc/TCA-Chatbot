import { mockSessions } from "@/data/mock";

export default function Sidebar() {
  return (
    <aside className="sidebar">

      <div className="sidebar-header">
        <h2 className="sidebar-title">
          Conversas
        </h2>
      </div>

      <button className="new-chat-btn">
        Nova Conversa
      </button>

      <div className="sessions-list">

        {mockSessions.map((session) => (
          <div
            key={session.id}
            className="session-card"
          >
            {session.title}
          </div>
        ))}

      </div>

    </aside>
  );
}