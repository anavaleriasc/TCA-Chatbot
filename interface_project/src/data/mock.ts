import { ChatSession } from "@/types/chat";

export const mockUser = {
  id: "1",
  name: "João",
  email: "joao@email.com",
};

export const mockSessions: ChatSession[] = [
  {
    id: "session-1",
    title: "Primeira conversa",
    messages: [
      {
        id: 1,
        sender: "user",
        text: "Olá",
      },
      {
        id: 2,
        sender: "bot",
        text: "Olá! Como posso ajudar?",
      },
    ],
  },
  {
    id: "session-2",
    title: "Dúvida AWS",
    messages: [
      {
        id: 1,
        sender: "user",
        text: "O que é EC2?",
      },
      {
        id: 2,
        sender: "bot",
        text: "EC2 é um serviço de máquinas virtuais da AWS.",
      },
    ],
  },
];