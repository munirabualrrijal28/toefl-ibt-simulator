import React, { useState, useEffect } from 'react';
import { Clock, User, ShieldCheck, AlertTriangle } from 'lucide-react';

interface ShellProps {
  children: React.ReactNode;
  title: string;
  totalSeconds: number;
  sectionName: string;
  onTimeUp?: () => void;
}

const Shell: React.FC<ShellProps> = ({ children, title, totalSeconds, sectionName, onTimeUp }) => {
  const [seconds, setSeconds] = useState(totalSeconds);

  useEffect(() => {
    setSeconds(totalSeconds);
  }, [totalSeconds]);

  useEffect(() => {
    if (seconds <= 0) {
      onTimeUp?.();
      return;
    }
    const timer = setInterval(() => setSeconds(s => s - 1), 1000);
    return () => clearInterval(timer);
  }, [seconds, onTimeUp]);

  const formatTime = (s: number) => {
    const mins = Math.floor(s / 60);
    const secs = s % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const pct = Math.max(0, (seconds / totalSeconds) * 100);
  const isWarning = seconds < 60;

  return (
    <div className="min-h-screen flex flex-col bg-[var(--color-toefl-background)]">
      {/* Header */}
      <header className="bg-gradient-to-r from-[var(--color-toefl-primary)] to-[var(--color-toefl-secondary)] text-white p-4 shadow-xl flex justify-between items-center px-8">
        <div className="flex items-center gap-3">
          <div className="bg-white/20 backdrop-blur-sm p-2 rounded-lg border border-white/20">
            <ShieldCheck size={22} />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight">TOEFL iBT Simulator</h1>
            <p className="text-[10px] opacity-70 uppercase tracking-[0.2em] font-semibold">2026 Secure Test Environment</p>
          </div>
        </div>

        <div className="flex items-center gap-5">
          <div className="text-right">
            <span className="block text-[10px] uppercase opacity-60 tracking-wider">Section</span>
            <span className="font-bold text-sm">{sectionName}</span>
          </div>
          <div className={`flex items-center gap-2 px-4 py-2 rounded-full border ${isWarning ? 'bg-red-500/30 border-red-300 animate-pulse' : 'bg-white/10 border-white/20'}`}>
            <Clock size={16} />
            <span className="text-lg font-mono font-bold tracking-wider">{formatTime(seconds)}</span>
          </div>
          <div className="w-9 h-9 rounded-full bg-white/15 flex items-center justify-center border border-white/25">
            <User size={18} />
          </div>
        </div>
      </header>

      {/* Timer Progress Bar */}
      <div className="h-1 bg-gray-200">
        <div
          className="h-full transition-all duration-1000 ease-linear"
          style={{ width: `${pct}%`, background: isWarning ? '#ef4444' : 'var(--color-toefl-accent)' }}
        />
      </div>

      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center p-6 overflow-y-auto">
        <div className="w-full max-w-4xl">
          <h2 className="text-xl font-bold text-[var(--color-toefl-dark)] mb-4">{title}</h2>
          <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 min-h-[480px] flex flex-col">
            {children}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 px-8 py-3 flex justify-between items-center text-xs text-gray-400">
        <div className="flex items-center gap-2">
          <AlertTriangle size={13} />
          <span>Test in progress — Do not close this window.</span>
        </div>
        <span>&copy; 2026 TOEFL iBT Simulator &middot; CEFR Aligned</span>
      </footer>
    </div>
  );
};

export default Shell;
