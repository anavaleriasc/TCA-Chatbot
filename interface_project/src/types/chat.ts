export interface Message {
  id: number;
  sender: "user" | "bot";
  text: string;
}

export interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
}