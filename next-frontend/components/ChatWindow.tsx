interface Message {
  role: 'user' | 'bot';
  text: string;
}

export default function ChatWindow({ messages }: { messages: Message[] }) {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-white rounded-xl shadow-inner">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`max-w-[80%] p-3 rounded-xl text-sm whitespace-pre-wrap ${
            msg.role === 'user'
              ? 'ml-auto bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-800'
          }`}
        >
          {msg.text}
        </div>
      ))}
    </div>
  );
} 