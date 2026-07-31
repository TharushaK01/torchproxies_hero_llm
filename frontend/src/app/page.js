// import ChatWidget from '@/components/ChatWidget';

// export default function Home() {
//   return (
//     <main className="min-h-screen flex flex-col items-center justify-center p-4">
//       <div className="w-full max-w-2xl text-center mb-6">
//         <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
//           Search faster, think deeper.
//         </h1>
//         <p className="text-slate-600 mt-2 text-sm">
//           Engage with our AI chatbot and discover a best proxies for your need.
//         </p>
//       </div>

//       <ChatWidget />
//     </main>
//   );
// }

import ChatWidget from '@/components/ChatWidget';
import { Check } from 'lucide-react';

export default function Home() {
  return (
    <main className="min-h-screen w-full bg-hero-radial relative flex items-center justify-center p-6 md:p-12 overflow-hidden">
      <div className="w-full max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center z-10">

        {/* Left Hero Section */}
        <div className="lg:col-span-6 flex flex-col justify-center space-y-8">
          <div className="space-y-4">
            <h1 
  style={{ fontFamily: "'Urbanist', sans-serif" }} 
  className="text-[42px] sm:text-7xl lg:text-[120px] font-normal tracking-tight text-white leading-[1.08]"
>
  <span className="text-orange-500 italic sm:not-italic">Unblock </span>
  every <br className="hidden sm:inline" />
  corner of{" "}
  <span className="text-orange-500 font-bold">the web.</span>
</h1>

            <p
              className="text-slate-200 text-base sm:text-lg max-w-lg pt-2 leading-relaxed font-regular"
            >
              Residential & ISP proxies for Shopify, sneaker, ticket sites with city targeting, ASN diversity, auto retry, real 10 Gbps lines.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-x-6 gap-y-3 text-xs sm:text-sm text-slate-200 font-regular">
            <div className="flex items-center gap-2">
              <Check className="text-orange-500 w-4 h-4 stroke-[3]" />
              <span>Rotating & Static IPs</span>
            </div>
            <div className="flex items-center gap-2">
              <Check className="text-orange-500 w-4 h-4 stroke-[3]" />
              <span>Unlimited Concurrency</span>
            </div>
            <div className="flex items-center gap-2">
              <Check className="text-orange-500 w-4 h-4 stroke-[3]" />
              <span>195+ Countries</span>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-wrap items-center gap-4 pt-2">
            <a
              href="#pricing"
              className="px-8 py-3.5 rounded-xl text-sm font-semibold text-slate-200 border border-slate-700/80 hover:border-slate-500 hover:bg-white/5 transition-all duration-200 text-center min-w-[140px]"
            >
              See Pricing
            </a>
            <a
              href="#start"
              className="px-8 py-3.5 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-orange-500 to-amber-600 hover:from-orange-600 hover:to-amber-700 shadow-lg shadow-orange-500/20 transition-all duration-200 text-center min-w-[140px]"
            >
              Start with 1GB
            </a>
          </div>
        </div>

        {/* Right Section: AI Chatbot Interface */}
        <div className="lg:col-span-6 flex flex-col items-center lg:items-end justify-center w-full">
          <div className="w-full max-w-xl space-y-4">
            <div className="text-center lg:text-left space-y-1">
              <h2 className="text-[22px] sm:text-[48px] font-regular text-white tracking-tight">
                Search faster, think deeper.
              </h2>
              <p className="text-slate-400 text-[12px] sm:text-[18px] max-w-[250px] text-center mx-auto sm:max-w-[580px]">
                Engage with our AI chatbot and discover the best proxies for your need.
              </p>
            </div>

            {/* Chat Widget Container */}
            <ChatWidget />
          </div>
        </div>

      </div>
    </main>
  );
}