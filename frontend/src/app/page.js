import ChatWidget from '@/components/ChatWidget';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-2xl text-center mb-6">
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
          Proxy AI Support Hub
        </h1>
        <p className="text-slate-600 mt-2 text-sm">
          Standalone client testing playground hooked directly to Gemma 3.
        </p>
      </div>

      <ChatWidget />
    </main>
  );
}
