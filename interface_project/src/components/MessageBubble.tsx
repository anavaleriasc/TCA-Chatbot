interface Props {
  text: string;
  sender: "user" | "bot";
}

export default function MessageBubble({
  text,
  sender,
}: Props) {
  return (
    <div
      className={`message ${sender}`}
    >
      {text}
    </div>
  );
}