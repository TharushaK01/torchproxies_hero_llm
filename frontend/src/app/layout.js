// import "./globals.css";

// export const metadata = {
//   title: "Proxy AI Chatbot",
//   description: "Standalone Local LLM interface",
// };

// export default function RootLayout({ children }) {
//   return (
//     <html lang="en">
//       <body className="antialiased bg-slate-100">
//         {children}
//       </body>
//     </html>
//   );
// }

import { Urbanist } from 'next/font/google';
import './globals.css';

const urbanist = Urbanist({ 
  subsets: ['latin'],
  weight: ['100', '200', '300', '400', '500', '600', '700', '800', '900'],
  variable: '--font-urbanist',
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={urbanist.variable}>
      <body className="font-sans antialiased">
        {children}
      </body>
    </html>
  );
}