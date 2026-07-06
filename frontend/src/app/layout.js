import "./globals.css";

export const metadata = {
  title: "Proxy AI Chatbot",
  description: "Standalone Local LLM interface",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="antialiased bg-slate-100">
        {children}
      </body>
    </html>
  );
}