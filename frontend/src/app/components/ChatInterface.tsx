import React, { useState } from 'react';
import { Send, Bot, User, Plus, Settings, Menu } from 'lucide-react';

interface Message {
  id: string;
  role: 'bot' | 'user';
  content: string;
}

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', role: 'bot', content: "Hello! I'm your AI assistant. How can I help you today?" }
  ]);
  const [input, setInput] = useState('');
  const [sessionId] = useState(() => Math.random().toString(36).substring(7));

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMessage: Message = { id: Date.now().toString(), role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    try {
      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, session_id: sessionId })
      });
      
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      
      setMessages(prev => [...prev, { id: (Date.now() + 1).toString(), role: 'bot', content: data.response }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { id: (Date.now() + 1).toString(), role: 'bot', content: "Sorry, I encountered an error." }]);
    }
  };

  return (
    <div className="flex h-screen bg-[#0f1117] text-gray-100 overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-[#1a1c23] border-r border-gray-800 flex flex-col p-4 hidden md:flex">
        <button className="flex items-center gap-3 w-full p-3 rounded-xl bg-blue-600 hover:bg-blue-700 transition-colors text-white font-medium mb-6">
          <Plus size={20} /> New Chat
        </button>
        <div className="flex-1 space-y-2 overflow-y-auto">
          <div className="text-xs font-semibold text-gray-500 uppercase px-2 mb-2">History</div>
          <div className="p-3 rounded-lg bg-[#252830] text-sm text-gray-300 cursor-pointer hover:bg-[#2d313a]">Current Session</div>
        </div>
        <button className="flex items-center gap-3 p-3 text-gray-400 hover:text-white transition-colors">
          <Settings size={20} /> Settings
        </button>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col h-full relative">
        {/* Header */}
        <header className="sticky top-0 bg-[#0f1117]/80 backdrop-blur-md border-b border-gray-800 p-4 flex items-center gap-3">
          <button className="md:hidden text-gray-400"><Menu /></button>
          <div className="bg-blue-600 p-2 rounded-xl text-white">
            <Bot size={20} />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-white">AI Assistant</h1>
            <div className="flex items-center gap-1 text-xs text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              Online
            </div>
          </div>
        </header>

        {/* Chat Area */}
        <main className="flex-1 overflow-y-auto p-4 md:p-8 space-y-8">
          {messages.map((m) => (
            <div key={m.id} className={`flex gap-4 ${m.role === 'user' ? 'justify-end' : ''}`}>
              {m.role === 'bot' && (
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-[#252830] flex items-center justify-center text-blue-400 border border-gray-700">
                  <Bot size={20} />
                </div>
              )}
              <div className={`p-5 rounded-2xl ${m.role === 'user' ? 'bg-blue-600 text-white rounded-tr-none shadow-lg shadow-blue-900/20' : 'bg-[#1a1c23] text-gray-200 rounded-tl-none border border-gray-800 shadow-xl'} max-w-[85%] md:max-w-2xl`}>
                {m.content}
              </div>
              {m.role === 'user' && (
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white border-2 border-blue-400">
                  <User size={20} />
                </div>
              )}
            </div>
          ))}
        </main>

        {/* Input Area */}
        <footer className="p-4 bg-[#0f1117]">
          <div className="max-w-4xl mx-auto flex items-center gap-2 bg-[#1a1c23] rounded-2xl p-2 border border-gray-800 focus-within:ring-2 focus-within:ring-blue-500/30 focus-within:border-blue-500 transition-all">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              className="flex-1 bg-transparent px-4 py-3 outline-none placeholder:text-gray-500"
              placeholder="Ask me anything..."
            />
            <button onClick={handleSend} className="bg-blue-600 text-white p-3 rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-600/20">
              <Send size={18} />
            </button>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default ChatInterface;
