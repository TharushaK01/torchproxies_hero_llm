"use client";

import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2 } from 'lucide-react';

export default function ChatWidget() {
  const [messages, setMessages] = useState([
    { role: 'system', content: 'Hello! I am your Proxy Support Assistant. How can I help you with your residential or datacenter proxy configurations today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

const updatedMessages = [...messages, { role: 'user', content: userMessage }];
setMessages(updatedMessages);

    try {
      const response = await fetch('http://127.0.0.1:8000/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ history: updatedMessages }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.log("Status:", response.status);
        console.log("Response:", errorText);
        // throw new Error(`Backend Error ${response.status}`);
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Setup stream reader to handle incoming data chunks from FastAPI
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      
      // Append an empty bot message slot into state that we fill live
      setMessages((prev) => [...prev, { role: 'assistant', content: '' }]);

      let accumulatedResponse = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const parsed = JSON.parse(line.slice(6));
              accumulatedResponse += parsed.response;
              
              // Updates the content of the very last message in real-time
              setMessages((prev) => {
                const updated = [...prev];
                updated[updated.length - 1].content = accumulatedResponse;
                return updated;
              });
            } catch (e) {
              // Ignore empty parsing anomalies or structural buffer noise
            }
          }
        }
      }
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev, 
        { role: 'assistant', content: "⚠️ Trouble connecting to the backend engine. Check your terminal to make sure the server is up." }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] w-full max-w-2xl mx-auto bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
      <div className="bg-slate-900 text-white p-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-600 rounded-lg"><Bot size={20} /></div>
          <div>
            <h2 className="font-semibold text-sm md:text-base">Proxy AI Support</h2>
            <p className="text-xs text-emerald-400 flex items-center gap-1">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              Gemma 3 Online
            </p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
        {messages.map((msg, index) => (
          <div key={index} className={`flex gap-3 max-w-[85%] ${msg.role === 'user' ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}>
            <div className={`p-2 h-8 w-8 rounded-full flex items-center justify-center shrink-0 text-white ${msg.role === 'user' ? 'bg-blue-600' : 'bg-slate-800'}`}>
              {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
            </div>
{/* The updated container with the smart markdown link parser inside */}
        <div className={`p-3 rounded-2xl shadow-sm ${msg.role === 'user' ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-white text-slate-800 border border-slate-100 rounded-tl-none'}`}>
          <div className="text-sm whitespace-pre-wrap leading-relaxed">
            {msg.content.split(/(\[[^\]]+\]\([^)]+\))/g).map((part, index) => {
              const match = part.match(/\[([^\]]+)\]\(([^)]+)\)/);
              if (match) {
                return (
                  <a 
                    key={index} 
                    href={match[2]} 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="inline-flex items-center mx-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded text-xs transition-colors duration-200 shadow-sm"
                  >
                    {match[1]}
                    <svg className="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                );
              }
              return part;
            })}
          </div>
        </div>
      </div>
    ))}
        {isLoading && messages[messages.length - 1]?.content === '' && (
          <div className="flex gap-3 max-w-[85%] mr-auto">
            <div className="p-2 h-8 w-8 rounded-full flex items-center justify-center bg-slate-800 text-white shrink-0"><Bot size={16} /></div>
            <div className="p-3 rounded-2xl bg-white border border-slate-100 rounded-tl-none flex items-center gap-2 text-slate-500 text-sm">
              <Loader2 size={16} className="animate-spin text-blue-600" /> Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} className="p-4 bg-white border-t border-slate-200 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about proxy pools, pricing, setup guides..."
          className="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500 bg-slate-50 text-slate-900"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()} className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-100 disabled:text-slate-400 text-white p-2.5 rounded-xl shrink-0">
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}