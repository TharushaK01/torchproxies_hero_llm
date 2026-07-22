import ChatWidget from '@/components/ChatWidget';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-2xl text-center mb-6">
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
          Search faster, think deeper.
        </h1>
        <p className="text-slate-600 mt-2 text-sm">
          Engage with our AI chatbot and discover a best proxies for your need.
        </p>
      </div>

      <ChatWidget />
    </main>
  );
}


// import ChatWidget from "@/components/ChatWidget";

// export default function Home() {
//   return (
//     <main className="relative min-h-screen overflow-hidden bg-[#0D0D0F] flex items-center justify-center px-6">

//       {/* Orange Glow */}
//       <div className="absolute -bottom-52 -left-52 w-[850px] h-[850px] rounded-full bg-orange-500 blur-[180px] opacity-80" />

//       {/* Dark Overlay */}
//       <div className="absolute inset-0 bg-gradient-to-b from-black/10 via-transparent to-black/20" />

//       {/* Content */}
//       <div className="relative z-10 w-full max-w-5xl text-center">
//         <h1 className="text-6xl font-extralight tracking-tight text-white">
//           Search faster, think deeper.
//         </h1>

//         <p className="mt-5 text-lg text-gray-400">
//           Engage with our AI chatbot and discover a best proxies for your need.
//         </p>

//         <div className="mt-12">
//           <ChatWidget />
//         </div>
//       </div>
//     </main>
//   );
// }