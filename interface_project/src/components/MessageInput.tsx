export default function MessageInput() {
  return (
    <div className="border-t p-4">
      <div className="flex gap-2">
        <input
          className="border p-2 flex-1"
          placeholder="Digite sua mensagem..."
        />

        <button className="border px-4">
          Enviar
        </button>
      </div>
    </div>
  );
}