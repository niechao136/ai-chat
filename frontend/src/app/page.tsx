'use client';
import { useState } from 'react';

type Message = {
  role: 'user' | 'ai';
  content: string;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;
    const newMessages: Message[] = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    
    const res = await fetch('/api/v1/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input, session_id: 'default' })
    });
    const data = await res.json();
    setMessages([...newMessages, { role: 'ai', content: data.response }]);
    setInput('');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-8">
      <h1 className="text-3xl font-bold mb-6">Gemini Chat</h1>
      <div className="w-full max-w-2xl bg-white p-6 rounded shadow-lg">
        <div className="h-96 overflow-y-auto mb-4 border-b pb-4">
          {messages.map((m, i) => (
            <div key={i} className={`mb-2 ${m.role === 'user' ? 'text-right text-blue-600' : 'text-left text-gray-800'}`}>
              <strong>{m.role === 'user' ? 'You' : 'AI'}:</strong> {m.content}
            </div>
          ))}
        </div>
        <div className="flex gap-2">
          <input 
            className="flex-1 border p-2 rounded"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type your message..."
          />
          <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}
