import React, { useState } from 'react';
import Taskbar from '../components/Taskbar';
import ChatWindow from '../components/ChatWindow';
import InputBox from '../components/InputBox';
import '../styles/elegant-chat.css';

interface Message {
  role: 'user' | 'bot';
  text: string;
}

export default function Home() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [messages, setMessages] = useState<Message[]>([]);

  const handleNewChat = () => {
    setMessages([]);
  };

  const handleToggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
    if (typeof document !== 'undefined') {
      document.documentElement.classList.toggle('dark');
    }
  };

  const sendMessage = (msg: string) => {
    setMessages((prev) => [
      ...prev,
      { role: 'user', text: msg },
      { role: 'bot', text: 'This is a bot reply.' }
    ]);
  };

  return (
    <div className={`elegant-container ${theme === 'dark' ? 'dark' : ''}`}>
      <Taskbar onNewChat={handleNewChat} onToggleTheme={handleToggleTheme} theme={theme} />
      <main className="elegant-main">
        {/* Sidebar/features */}
        <aside className="elegant-sidebar">
          <div className="font-semibold text-gray-700 mb-2">Features</div>
          <ul className="elegant-features-list">
            <li className="active">Dashboard</li>
            <li>History</li>
            <li>Upload Document</li>
            <li>Export Chat</li>
            <li>Settings</li>
            <li>Help & Support</li>
            <li>Integrations</li>
            <li>API Keys</li>
            <li>Analytics</li>
          </ul>
        </aside>
        {/* Chatbot area */}
        <section className="elegant-chat-area w-full flex flex-col flex-1">
          <div className="flex flex-col flex-1 bg-gray-50 rounded-xl overflow-hidden shadow">
            <ChatWindow messages={messages} />
            <InputBox onSend={sendMessage} />
          </div>
        </section>
      </main>
    </div>
  );
} 