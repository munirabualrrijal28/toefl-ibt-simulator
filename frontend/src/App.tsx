import React, { useState, useCallback, useRef } from 'react';
import Shell from './components/Shell';
import { sessionService } from './services/api';
import { BookOpen, Headphones, PenLine, Mic, Trophy, ArrowRight, Square, RotateCcw } from 'lucide-react';

/* ── Types ── */
interface Question {
  id: string;
  section: string;
  task_type: string;
  difficulty_pool: string;
  content_meta: any;
  correct_answer_key: string | null;
}
interface SectionState {
  id: number;
  session_id: string;
  section_name: string;
  stage: string;
  is_done: boolean;
}

/* ── Section time limits (seconds) ── */
const SECTION_TIME: Record<string, number> = {
  Reading: 30 * 60,
  Listening: 29 * 60,
  Writing: 23 * 60,
  Speaking: 8 * 60,
};

const SECTION_ICON: Record<string, React.ReactNode> = {
  Reading:   <BookOpen size={18} />,
  Listening: <Headphones size={18} />,
  Writing:   <PenLine size={18} />,
  Speaking:  <Mic size={18} />,
};

/* ═══════════════════════════════════════════════
   APP COMPONENT
   ═══════════════════════════════════════════════ */
const App: React.FC = () => {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [currentSection, setCurrentSection] = useState<SectionState | null>(null);
  const [currentItem, setCurrentItem] = useState<Question | null>(null);
  const [loading, setLoading] = useState(false);
  const [isTestStarted, setIsTestStarted] = useState(false);
  const [testResult, setTestResult] = useState<any>(null);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [textValue, setTextValue] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /* ── Recording state (Speaking) ── */
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const recordingTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  /* ── Start Test ── */
  const startTest = async () => {
    setError(null);
    try {
      const res = await sessionService.startSession();
      setSessionId(res.data.id);
      setIsTestStarted(true);
      fetchState(res.data.id);
    } catch (err) {
      setError("Failed to start session. Is the backend running?");
    }
  };

  /* ── Fetch current state + next item ── */
  const fetchState = async (id: string) => {
    setLoading(true);
    setSelectedOption(null);
    setTextValue('');
    try {
      const stateRes = await sessionService.getCurrentState(id);
      setCurrentSection(stateRes.data);
      const itemRes = await sessionService.getNextItem(id);
      setCurrentItem(itemRes.data);
    } catch (err: any) {
      if (err.response?.status === 404) {
        const scoreRes = await sessionService.getScore(id);
        setTestResult(scoreRes.data);
      } else {
        setError("Error fetching test data.");
      }
    } finally {
      setLoading(false);
    }
  };

  /* ── Submit answer ── */
  const handleSubmit = async (payload: { text_payload?: string }) => {
    if (!sessionId || !currentItem || submitting) return;
    setSubmitting(true);
    try {
      await sessionService.submitResponse(sessionId, currentItem.id, payload);
      fetchState(sessionId);
    } catch (err) {
      setError("Submission failed.");
    } finally {
      setSubmitting(false);
    }
  };

  /* ── Mic Recording ── */
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mr = new MediaRecorder(stream);
      mediaRecorderRef.current = mr;
      mr.start();
      setIsRecording(true);
      setRecordingTime(0);
      recordingTimerRef.current = setInterval(() => setRecordingTime(t => t + 1), 1000);
    } catch {
      setError("Microphone access denied.");
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    mediaRecorderRef.current?.stream.getTracks().forEach(t => t.stop());
    setIsRecording(false);
    if (recordingTimerRef.current) clearInterval(recordingTimerRef.current);
    handleSubmit({ text_payload: `[audio_recording_${recordingTime}s]` });
  };

  /* ── Time up handler ── */
  const handleTimeUp = useCallback(() => {
    if (sessionId) fetchState(sessionId);
  }, [sessionId]);

  /* ═══════════════ LANDING SCREEN ═══════════════ */
  if (!isTestStarted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 flex items-center justify-center p-6">
        <div className="max-w-lg w-full">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-cyan-400 to-blue-600 mb-4 shadow-lg shadow-blue-500/30">
              <ShieldCheck size={32} className="text-white" />
            </div>
            <h1 className="text-4xl font-extrabold text-white tracking-tight">TOEFL iBT</h1>
            <p className="text-cyan-300 font-semibold text-sm tracking-[0.15em] uppercase mt-1">2026 Adaptive Edition</p>
          </div>

          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8 space-y-6">
            <p className="text-gray-300 text-sm text-center leading-relaxed">
              Multistage adaptive simulation aligned to CEFR band scoring (1.0 – 6.0).
            </p>

            <div className="space-y-3">
              {[
                { name: 'Reading', time: '30 min', desc: 'Adaptive routing', icon: <BookOpen size={16} /> },
                { name: 'Listening', time: '29 min', desc: 'Adaptive routing', icon: <Headphones size={16} /> },
                { name: 'Writing', time: '23 min', desc: 'Fixed path', icon: <PenLine size={16} /> },
                { name: 'Speaking', time: '8 min', desc: 'Fixed path', icon: <Mic size={16} /> },
              ].map(s => (
                <div key={s.name} className="flex items-center gap-3 bg-white/5 px-4 py-3 rounded-xl border border-white/5">
                  <div className="text-cyan-400">{s.icon}</div>
                  <div className="flex-1">
                    <span className="text-white font-semibold text-sm">{s.name}</span>
                    <span className="text-gray-500 text-xs ml-2">{s.desc}</span>
                  </div>
                  <span className="text-gray-400 text-xs font-mono">{s.time}</span>
                </div>
              ))}
            </div>

            {error && <p className="text-red-400 text-sm text-center">{error}</p>}

            <button
              onClick={startTest}
              className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold py-4 rounded-xl shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 text-lg"
            >
              Start Simulation <ArrowRight size={20} />
            </button>
          </div>
        </div>
      </div>
    );
  }

  /* ═══════════════ RESULTS SCREEN ═══════════════ */
  if (testResult) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 flex items-center justify-center p-6">
        <div className="max-w-2xl w-full">
          <div className="text-center mb-8">
            <Trophy size={48} className="text-amber-400 mx-auto mb-3" />
            <h1 className="text-3xl font-bold text-white uppercase tracking-widest">Test Complete</h1>
          </div>
          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-8 space-y-8">
            <div className="text-center">
              <p className="text-xs uppercase tracking-[0.2em] text-gray-400 mb-2">Overall CEFR Band Score</p>
              <div className="text-8xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
                {testResult.overall_score?.toFixed(1) ?? '—'}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              {testResult.sections?.map((s: any) => (
                <div key={s.id} className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                  <p className="text-[10px] font-bold uppercase text-gray-500 tracking-wider">{s.section_name}</p>
                  <p className="text-3xl font-black text-white mt-1">{s.band_score?.toFixed(1) ?? '—'}</p>
                  <p className="text-[10px] text-gray-500 mt-1">{s.stage}</p>
                </div>
              ))}
            </div>
            <button
              onClick={() => window.location.reload()}
              className="w-full flex items-center justify-center gap-2 bg-white/10 border border-white/20 text-white font-semibold py-3 rounded-xl hover:bg-white/20 transition-all"
            >
              <RotateCcw size={16} /> Take Another Test
            </button>
          </div>
        </div>
      </div>
    );
  }

  /* ═══════════════ LOADING ═══════════════ */
  if (loading || !currentSection || !currentItem) {
    return (
      <div className="min-h-screen bg-[var(--color-toefl-background)] flex flex-col items-center justify-center gap-4">
        <div className="w-10 h-10 border-4 border-[var(--color-toefl-primary)] border-t-transparent rounded-full animate-spin" />
        <p className="font-semibold text-[var(--color-toefl-primary)]">Loading test environment…</p>
      </div>
    );
  }

  /* ═══════════════ RENDER QUESTION CONTENT ═══════════════ */
  const renderQuestion = () => {
    const meta = currentItem!.content_meta;
    const section = currentItem!.section;
    const taskType = currentItem!.task_type;

    /* ── READING: Complete Words ── */
    if (taskType === 'COMPLETE_WORDS') {
      return (
        <div className="flex-1 flex flex-col space-y-6">
          <div className="bg-slate-50 p-6 rounded-xl border border-slate-200">
            <p className="text-lg leading-relaxed font-serif">{meta.passage}</p>
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-600 mb-2">Fill in the missing words (comma-separated):</label>
            <input
              type="text"
              value={textValue}
              onChange={e => setTextValue(e.target.value)}
              className="w-full max-w-md p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[var(--color-toefl-primary)] focus:border-transparent outline-none transition-all"
              placeholder="e.g. fox,lazy"
            />
          </div>
          <div className="flex justify-end mt-auto">
            <button
              onClick={() => handleSubmit({ text_payload: textValue })}
              disabled={!textValue.trim() || submitting}
              className="flex items-center gap-2 bg-[var(--color-toefl-primary)] text-white font-semibold px-6 py-3 rounded-xl hover:bg-[var(--color-toefl-secondary)] disabled:opacity-40 transition-all"
            >
              Submit <ArrowRight size={16} />
            </button>
          </div>
        </div>
      );
    }

    /* ── READING / LISTENING: Multiple Choice ── */
    if (meta.options) {
      return (
        <div className="flex-1 flex flex-col space-y-6">
          {meta.passage && (
            <div className="bg-slate-50 p-6 rounded-xl border border-slate-200">
              <p className="text-lg leading-relaxed font-serif">{meta.passage}</p>
            </div>
          )}
          {meta.transcript && (
            <div className="bg-blue-50 p-4 rounded-xl border border-blue-100">
              <p className="text-xs text-blue-500 font-bold uppercase mb-1">{section === 'Listening' ? '🎧 Audio Transcript (simulated)' : 'Context'}</p>
              <p className="text-gray-700 italic">"{meta.transcript}"</p>
            </div>
          )}
          <p className="text-xl font-bold text-[var(--color-toefl-dark)]">{meta.question}</p>
          <div className="space-y-3">
            {meta.options.map((opt: string, i: number) => (
              <button
                key={opt}
                onClick={() => setSelectedOption(opt)}
                className={`w-full text-left p-4 rounded-xl border-2 transition-all duration-150 flex items-center gap-3
                  ${selectedOption === opt
                    ? 'border-[var(--color-toefl-primary)] bg-blue-50 shadow-md'
                    : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
              >
                <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold shrink-0
                  ${selectedOption === opt ? 'bg-[var(--color-toefl-primary)] text-white' : 'bg-gray-100 text-gray-500'}`}>
                  {String.fromCharCode(65 + i)}
                </span>
                <span className="font-medium">{opt}</span>
              </button>
            ))}
          </div>
          <div className="flex justify-end mt-auto">
            <button
              onClick={() => handleSubmit({ text_payload: selectedOption! })}
              disabled={!selectedOption || submitting}
              className="flex items-center gap-2 bg-[var(--color-toefl-primary)] text-white font-semibold px-6 py-3 rounded-xl hover:bg-[var(--color-toefl-secondary)] disabled:opacity-40 transition-all"
            >
              Next <ArrowRight size={16} />
            </button>
          </div>
        </div>
      );
    }

    /* ── WRITING: Build a Sentence ── */
    if (taskType === 'BUILD_SENTENCE') {
      return (
        <div className="flex-1 flex flex-col space-y-6">
          <p className="font-semibold text-gray-600">Arrange these words into a correct sentence:</p>
          <div className="flex flex-wrap gap-2">
            {meta.scrambled_words?.map((w: string, i: number) => (
              <span key={i} className="bg-blue-100 text-blue-800 px-4 py-2 rounded-lg font-semibold text-lg border border-blue-200 cursor-pointer hover:bg-blue-200 transition-colors">{w}</span>
            ))}
          </div>
          <div>
            <input
              type="text"
              value={textValue}
              onChange={e => setTextValue(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[var(--color-toefl-primary)] focus:border-transparent outline-none"
              placeholder="Type the correct sentence here..."
            />
          </div>
          <div className="flex justify-end mt-auto">
            <button
              onClick={() => handleSubmit({ text_payload: textValue })}
              disabled={!textValue.trim() || submitting}
              className="flex items-center gap-2 bg-[var(--color-toefl-primary)] text-white font-semibold px-6 py-3 rounded-xl hover:bg-[var(--color-toefl-secondary)] disabled:opacity-40 transition-all"
            >
              Submit <ArrowRight size={16} />
            </button>
          </div>
        </div>
      );
    }

    /* ── WRITING: Email & Academic Discussion ── */
    if (taskType === 'WRITE_EMAIL' || taskType === 'ACADEMIC_DISCUSSION') {
      return (
        <div className="flex-1 flex flex-col space-y-5">
          <div className="bg-slate-50 p-5 rounded-xl border border-slate-200">
            <p className="text-lg font-semibold">{meta.prompt}</p>
            {meta.bullets && (
              <ul className="mt-3 space-y-1">
                {meta.bullets.map((b: string, i: number) => (
                  <li key={i} className="text-gray-600 text-sm flex items-start gap-2">
                    <span className="text-[var(--color-toefl-primary)] font-bold mt-0.5">•</span> {b}
                  </li>
                ))}
              </ul>
            )}
            {meta.context && <p className="mt-3 text-gray-500 text-sm italic">{meta.context}</p>}
          </div>
          <textarea
            value={textValue}
            onChange={e => setTextValue(e.target.value)}
            className="flex-1 min-h-[200px] p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-[var(--color-toefl-primary)] focus:border-transparent outline-none resize-none"
            placeholder="Write your response here..."
          />
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-400">{textValue.split(/\s+/).filter(Boolean).length} words</span>
            <button
              onClick={() => handleSubmit({ text_payload: textValue })}
              disabled={textValue.trim().length < 10 || submitting}
              className="flex items-center gap-2 bg-[var(--color-toefl-primary)] text-white font-semibold px-6 py-3 rounded-xl hover:bg-[var(--color-toefl-secondary)] disabled:opacity-40 transition-all"
            >
              Submit Response <ArrowRight size={16} />
            </button>
          </div>
        </div>
      );
    }

    /* ── SPEAKING: Listen & Repeat / Interview ── */
    if (section === 'Speaking') {
      return (
        <div className="flex-1 flex flex-col items-center justify-center space-y-8 py-8">
          {meta.phrase && (
            <div className="bg-blue-50 p-5 rounded-xl border border-blue-100 text-center max-w-md">
              <p className="text-xs text-blue-500 font-bold uppercase mb-2">Listen & Repeat</p>
              <p className="text-lg font-semibold text-gray-800">"{meta.phrase}"</p>
            </div>
          )}
          {meta.turns && (
            <div className="bg-blue-50 p-5 rounded-xl border border-blue-100 text-center max-w-md">
              <p className="text-xs text-blue-500 font-bold uppercase mb-2">Interview Question</p>
              <p className="text-lg font-semibold text-gray-800">"{meta.turns[0]?.prompt}"</p>
            </div>
          )}

          {!isRecording ? (
            <button
              onClick={startRecording}
              className="w-24 h-24 rounded-full bg-gradient-to-br from-red-500 to-red-600 flex items-center justify-center text-white shadow-xl shadow-red-500/30 hover:scale-105 active:scale-95 transition-transform"
            >
              <Mic size={36} />
            </button>
          ) : (
            <div className="flex flex-col items-center gap-4">
              <div className="w-24 h-24 rounded-full bg-red-500 flex items-center justify-center text-white animate-pulse shadow-xl shadow-red-500/40">
                <span className="font-mono font-bold text-lg">{recordingTime}s</span>
              </div>
              <button
                onClick={stopRecording}
                className="flex items-center gap-2 bg-gray-800 text-white font-semibold px-6 py-3 rounded-xl hover:bg-gray-700 transition-all"
              >
                <Square size={16} /> Stop & Submit
              </button>
            </div>
          )}

          <p className="text-gray-400 text-sm">
            {isRecording ? 'Recording in progress — speak clearly.' : 'Click the microphone to start recording.'}
          </p>
        </div>
      );
    }

    /* ── Fallback ── */
    return (
      <div className="flex-1 flex flex-col space-y-4">
        <pre className="bg-gray-50 p-4 rounded-xl text-sm overflow-auto">{JSON.stringify(meta, null, 2)}</pre>
        <button
          onClick={() => handleSubmit({ text_payload: "skip" })}
          className="self-end flex items-center gap-2 bg-[var(--color-toefl-primary)] text-white font-semibold px-6 py-3 rounded-xl"
        >
          Skip <ArrowRight size={16} />
        </button>
      </div>
    );
  };

  /* ═══════════════ MAIN TEST VIEW ═══════════════ */
  const stageLabel = currentSection.stage === 'ROUTING' ? 'Routing Stage'
    : currentSection.stage === 'ADAPTIVE_B_HARD' ? 'Adaptive Stage (Academic — Hard)'
    : currentSection.stage === 'ADAPTIVE_A_STANDARD' ? 'Adaptive Stage (Standard)'
    : 'Fixed Path';

  return (
    <Shell
      sectionName={currentSection.section_name}
      totalSeconds={SECTION_TIME[currentSection.section_name] || 30 * 60}
      title={`${currentSection.section_name} — ${stageLabel}`}
      onTimeUp={handleTimeUp}
    >
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded-lg mb-4 text-sm">
          {error}
        </div>
      )}
      <div className="flex items-center gap-2 mb-4 text-xs">
        <span className="flex items-center gap-1 text-[var(--color-toefl-primary)]">{SECTION_ICON[currentItem.section]}</span>
        <span className="text-gray-400 uppercase tracking-wider font-semibold">{currentItem.task_type.replace(/_/g, ' ')}</span>
        <span className="ml-auto text-gray-300 text-[10px] font-mono">{currentItem.difficulty_pool}</span>
      </div>
      {renderQuestion()}
    </Shell>
  );
};

/* ── Missing import used in landing ── */
const ShieldCheck: React.FC<{ size: number; className?: string }> = ({ size, className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    <path d="m9 12 2 2 4-4"/>
  </svg>
);

export default App;
