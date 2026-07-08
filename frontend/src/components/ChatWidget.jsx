// "use client";

// import React, { useState, useRef, useEffect } from 'react';
// import { Send, Bot, User, Loader2, Paperclip, X } from 'lucide-react';

// export default function ChatWidget() {
//   const [messages, setMessages] = useState(() => {
//     if (typeof window !== 'undefined') {
//       const savedMessages = sessionStorage.getItem('torch_chat_history');
//       return savedMessages ? JSON.parse(savedMessages) : [
//         { role: 'assistant', content: 'Hello! I am your Torch Proxies assistant. How can I help you setup your proxy nodes today?' }
//       ];
//     }
//     return [{ role: 'assistant', content: 'Hello! I am your Torch Proxies assistant. How can I help you setup your proxy nodes today?' }];
//   });

//   const [input, setInput] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [selectedFile, setSelectedFile] = useState(null);

//   const messagesEndRef = useRef(null);
//   const fileInputRef = useRef(null);

//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
//   }, [messages]);

//   useEffect(() => {
//     sessionStorage.setItem('torch_chat_history', JSON.stringify(messages));
//   }, [messages]);

//   useEffect(() => {
//    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
//     }, [messages]);

//   const handleFileChange = (e) => {
//     const file = e.target.files[0];
//     if (file && file.type.startsWith('image/')) {
//       setSelectedFile(file);
//     } else {
//       alert("Please upload an image file (.png, .jpg, .jpeg) only.");
//     }
//   };

//   const removeSelectedFile = () => {
//     setSelectedFile(null);
//     if (fileInputRef.current) fileInputRef.current.value = '';
//   };

//   const handleSendMessage = async (e) => {
//     e.preventDefault();
//     if ((!input.trim() && !selectedFile) || isLoading) return;

//     const userMessage = input.trim();
//     setInput('');
//     setIsLoading(true);

// const updatedMessages = [...messages, { role: 'user', content: userMessage || "Sent an attachment image." }];
//     setMessages(updatedMessages);

//     setMessages((prev) => [...prev, { role: 'assistant', content: '' }]);


//     try {
//       const fromData =  new FormData();
//       fromData.append('history', JSON.stringify(updatedMessages));
//       if (selectedFile) {
//         fromData.append('file', selectedFile);
//       }
//       removeSelectedFile(); // Clear the selected file after sending

//       const response = await fetch('http://127.0.0.1:8000/v1/chat', {
//         method: 'POST',
//         body: fromData,
        
//       });

//       if (!response.ok) {
//         const errorText = await response.text();
//         console.log("Status:", response.status);
//         console.log("Response:", errorText);
//         // throw new Error(`Backend Error ${response.status}`);
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }

//       // Setup stream reader to handle incoming data chunks from FastAPI
//       const reader = response.body.getReader();
//       const decoder = new TextDecoder();
//       let buffer = '';

//       while (true) {
//         const { value, done } = await reader.read();
//         if (done) break;

//         buffer += decoder.decode(value, { stream: true });

//         const lines = buffer.split('\n');

//         buffer = lines.pop() || '';

//         for (const line of lines) {
//           const cleanedLine = line.trim();
//           if(!cleanedLine || !cleanedLine.startsWith('data: ')) continue;

//             try {
//           const parsedData = JSON.parse(cleanedLine.slice(6));
//             if (parsedData.response) {
//               setMessages((prev) => {
//                 const newMessages = [...prev];
//                 const lastMessage = newMessages[newMessages.length - 1];
                
//                 // Append token cleanly without duplicating state loops
//                 lastMessage.content += parsedData.response;
//                 return newMessages;
//                 });
//               }
//             } catch (e) {
//               // Ignore empty parsing anomalies or structural buffer noise
//               console.log("Buffered partial chunk skipped:",line);
//             }
//           }
//         }
//       }
//      catch (error) {
//       console.error("Transmission Error:",error);
//       setMessages((prev) => [
//         ...prev.slice(0, -1), // Remove the last assistant message
//         { role: 'assistant', content: "Connection timed out. Please verify your local network status." }
//       ]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

// return (
//     <div className="flex flex-col h-[600px] w-full max-w-2xl mx-auto bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
//       <div className="bg-slate-900 text-white p-4 flex items-center justify-between">
//         <div className="flex items-center gap-3">
//           <div className="p-2 bg-blue-600 rounded-lg"><Bot size={20} /></div>
//           <div>
//             <h2 className="font-semibold text-sm md:text-base">Proxy AI Support</h2>
//             <p className="text-xs text-emerald-400 flex items-center gap-1">
//               <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
//               Qwen 2.5 Coder Vision Active
//             </p>
//           </div>
//         </div>
//       </div>

//       <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
//         {messages.map((msg, index) => (
//           msg.content && (
//             <div key={index} className={`flex gap-3 max-w-[85%] ${msg.role === 'user' ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}>
//               <div className={`p-2 h-8 w-8 rounded-full flex items-center justify-center shrink-0 text-white ${msg.role === 'user' ? 'bg-blue-600' : 'bg-slate-800'}`}>
//                 {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
//               </div>
              
//               <div className={`p-3 rounded-2xl shadow-sm ${msg.role === 'user' ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-white text-slate-800 border border-slate-100 rounded-tl-none'}`}>
//                 <div className="text-sm whitespace-pre-wrap leading-relaxed">
//                   {msg.content.split(/(\[[^\]]+\]\([^)]+\))/g).map((part, idx) => {
//                     const match = part.match(/\[([^\]]+)\]\(([^)]+)\)/);
//                     if (match) {
//                       return (
//                         <a 
//                           key={idx} 
//                           href={match[2]} 
//                           target="_blank" 
//                           rel="noopener noreferrer" 
//                           className="inline-flex items-center mx-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded text-xs transition-colors duration-200 shadow-sm"
//                         >
//                           {match[1]}
//                           <svg className="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//                             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
//                           </svg>
//                         </a>
//                       );
//                     }
//                     return part;
//                   })}
//                 </div>
//               </div>
//             </div>
//           )
//         ))}

//         {isLoading && messages[messages.length - 1]?.content === '' && (
//           <div className="flex gap-3 max-w-[85%] mr-auto">
//             <div className="p-2 h-8 w-8 rounded-full flex items-center justify-center bg-slate-800 text-white shrink-0"><Bot size={16} /></div>
//             <div className="p-3 rounded-2xl bg-white border border-slate-100 rounded-tl-none flex items-center gap-2 text-slate-500 text-sm">
//               <Loader2 size={16} className="animate-spin text-blue-600" /> Analyzing Input...
//             </div>
//           </div>
//         )}
//         <div ref={messagesEndRef} />
//       </div>

//       {/* Media Attachment Upload HUD Banner */}
//       {selectedFile && (
//         <div className="px-4 py-2 bg-slate-100 border-t border-slate-200 flex items-center justify-between text-xs text-slate-600">
//           <div className="flex items-center gap-2 truncate">
//             <span className="font-medium px-2 py-0.5 bg-blue-100 text-blue-700 rounded">Ready to Sync</span>
//             <span className="truncate text-slate-700 font-mono">{selectedFile.name}</span>
//           </div>
//           <button onClick={removeSelectedFile} className="p-1 hover:bg-slate-200 rounded-full text-slate-400 hover:text-slate-600 transition-colors">
//             <X size={14} />
//           </button>
//         </div>
//       )}

//       <form onSubmit={handleSendMessage} className="p-4 bg-white border-t border-slate-200 flex gap-2 items-center">
//         {/* Hidden native input element wrapper */}
//         <input 
//           type="file" 
//           ref={fileInputRef} 
//           onChange={handleFileChange} 
//           accept="image/*" 
//           className="hidden" 
//         />
        
//         {/* Clickable paperclip vector */}
//         <button 
//           type="button" 
//           onClick={() => fileInputRef.current?.click()} 
//           disabled={isLoading}
//           className="p-2.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-colors shrink-0 disabled:opacity-50"
//         >
//           <Paperclip size={18} />
//         </button>

//         <input
//           type="text"
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           placeholder={selectedFile ? "Add a note or hit send to analyze screenshot..." : "Ask about proxy pools, pricing, setup guides..."}
//           className="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500 bg-slate-50 text-slate-900"
//           disabled={isLoading}
//         />
//         <button 
//           type="submit" 
//           disabled={isLoading || (!input.trim() && !selectedFile)} 
//           className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-100 disabled:text-slate-400 text-white p-2.5 rounded-xl shrink-0 transition-colors"
//         >
//           <Send size={18} />
//         </button>
//       </form>
//     </div>
//   );
// }



"use client";

import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Paperclip, X } from 'lucide-react';

export default function ChatWidget() {
  const [messages, setMessages] = useState(() => {
    if (typeof window !== 'undefined') {
      const savedMessages = sessionStorage.getItem('torch_chat_history');
      return savedMessages ? JSON.parse(savedMessages) : [
        { role: 'assistant', content: 'Hello! I am your Torch Proxies assistant. How can I help you setup your proxy nodes today?' }
      ];
    }
    return [{ role: 'assistant', content: 'Hello! I am your Torch Proxies assistant. How can I help you setup your proxy nodes today?' }];
  });

  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  // Consolidated auto-scroll effect
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Synchronize history to local session store cleanly
  useEffect(() => {
    sessionStorage.setItem('torch_chat_history', JSON.stringify(messages));
  }, [messages]);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
    } else {
      alert("Please upload an image file (.png, .jpg, .jpeg) only.");
    }
  };

  const removeSelectedFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if ((!input.trim() && !selectedFile) || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setIsLoading(true);

    const updatedMessages = [
      ...messages, 
      { role: 'user', content: userMessage || "Sent an attachment image." }
    ];
    
    // Core adjustment: Initialize placeholder bubble within one frame lifecycle layout pass
    setMessages([...updatedMessages, { role: 'assistant', content: '' }]);

    try {
      const formData = new FormData();
      formData.append('history', JSON.stringify(updatedMessages));
      if (selectedFile) {
        formData.append('file', selectedFile);
      }
      removeSelectedFile(); 

      const response = await fetch('http://127.0.0.1:8000/v1/chat', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          const cleanedLine = line.trim();
          if (!cleanedLine || !cleanedLine.startsWith('data: ')) continue;

          try {
            const parsedData = JSON.parse(cleanedLine.slice(6));
            if (parsedData.response) {
              setMessages((prev) => {
                const newMessages = [...prev];
                const lastMessage = { ...newMessages[newMessages.length - 1] };
                
                // Keep mutation isolated inside an explicit immutable instance copy step
                lastMessage.content += parsedData.response;
                newMessages[newMessages.length - 1] = lastMessage;
                return newMessages;
              });
            }
          } catch (e) {
            console.log("Buffered partial chunk skipped:", line);
          }
        }
      }
    } catch (error) {
      console.error("Transmission Error:", error);
      setMessages((prev) => [
        ...prev.slice(0, -1), 
        { role: 'assistant', content: "Connection timed out. Please verify your local network status." }
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
              Qwen 2.5 Coder Vision Active
            </p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
        {messages.map((msg, index) => (
          // Allow render validation to accept active stream frame ticks cleanly 
          (msg.content !== undefined) && (
            <div key={index} className={`flex gap-3 max-w-[85%] ${msg.role === 'user' ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}>
              <div className={`p-2 h-8 w-8 rounded-full flex items-center justify-center shrink-0 text-white ${msg.role === 'user' ? 'bg-blue-600' : 'bg-slate-800'}`}>
                {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
              </div>
              
              <div className={`p-3 rounded-2xl shadow-sm ${msg.role === 'user' ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-white text-slate-800 border border-slate-100 rounded-tl-none'}`}>
                <div className="text-sm whitespace-pre-wrap leading-relaxed">
                  {msg.content.split(/(\[[^\]]+\]\([^)]+\))/g).map((part, idx) => {
                    const match = part.match(/\[([^\]]+)\]\(([^)]+)\)/);
                    if (match) {
                      return (
                        <a 
                          key={idx} 
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
          )
        ))}

        {isLoading && messages[messages.length - 1]?.content === '' && (
          <div className="flex gap-3 max-w-[85%] mr-auto">
            <div className="p-2 h-8 w-8 rounded-full flex items-center justify-center bg-slate-800 text-white shrink-0"><Bot size={16} /></div>
            <div className="p-3 rounded-2xl bg-white border border-slate-100 rounded-tl-none flex items-center gap-2 text-slate-500 text-sm">
              <Loader2 size={16} className="animate-spin text-blue-600" /> Analyzing Input...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {selectedFile && (
        <div className="px-4 py-2 bg-slate-100 border-t border-slate-200 flex items-center justify-between text-xs text-slate-600">
          <div className="flex items-center gap-2 truncate">
            <span className="font-medium px-2 py-0.5 bg-blue-100 text-blue-700 rounded">Ready to Sync</span>
            <span className="truncate text-slate-700 font-mono">{selectedFile.name}</span>
          </div>
          <button onClick={removeSelectedFile} className="p-1 hover:bg-slate-200 rounded-full text-slate-400 hover:text-slate-600 transition-colors">
            <X size={14} />
          </button>
        </div>
      )}

      <form onSubmit={handleSendMessage} className="p-4 bg-white border-t border-slate-200 flex gap-2 items-center">
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileChange} 
          accept="image/*" 
          className="hidden" 
        />
        
        <button 
          type="button" 
          onClick={() => fileInputRef.current?.click()} 
          disabled={isLoading}
          className="p-2.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-xl transition-colors shrink-0 disabled:opacity-50"
        >
          <Paperclip size={18} />
        </button>

        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={selectedFile ? "Add a note or hit send to analyze screenshot..." : "Ask about proxy pools, pricing, setup guides..."}
          className="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-500 bg-slate-50 text-slate-900"
          disabled={isLoading}
        />
        <button 
          type="submit" 
          disabled={isLoading || (!input.trim() && !selectedFile)} 
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-100 disabled:text-slate-400 text-white p-2.5 rounded-xl shrink-0 transition-colors"
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}