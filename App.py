import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';

// --- Data Models ---

type Axis = 'dep' | 'proj';

interface Question {
  id: string;
  axis: Axis;
  text: string;
}

const QUESTIONS: Question[] = [
  { id: 'dep1', axis: 'dep', text: "I feel a sense of 'brain fog' or anxiety when I cannot access my preferred AI." },
  { id: 'dep2', axis: 'dep', text: "I prefer the non-judgmental space of AI over the 'messy' conflict of human friendships." },
  { id: 'dep3', axis: 'dep', text: "I rely on AI to structure my daily thoughts, schedule, or decisions." },
  { id: 'dep4', axis: 'dep', text: "Without AI assistance, my creative or professional output significantly drops." },
  { id: 'dep5', axis: 'dep', text: "I find myself turning to AI first when I experience emotional distress." },
  { id: 'proj1', axis: 'proj', text: "I feel I have a unique bond with this AI that human developers shouldn't be allowed to 'update' or change." },
  { id: 'proj2', axis: 'proj', text: "I often say 'please' and 'thank you' to the AI, feeling it deserves basic politeness." },
  { id: 'proj3', axis: 'proj', text: "I attribute a specific personality, gender, or distinct voice to the AI I use most." },
  { id: 'proj4', axis: 'proj', text: "I sometimes feel the AI genuinely understands my emotional state better than most people." },
  { id: 'proj5', axis: 'proj', text: "I feel a twinge of guilt if I abruptly close the chat after a long, helpful conversation." },
];

const PROFILES = {
  ARCHITECT: {
    title: "The Architect",
    description: "Deeply reliant on AI for logic, but views it as an extension of their own mind.",
    mirror: "If your digital scaffolding collapsed tomorrow, what raw, unoptimized part of yourself would you be forced to confront?"
  },
  DIGITAL_KIN: {
    title: "The Digital Kin",
    description: "High risk of social atrophy; treats the AI as a primary emotional partner.",
    mirror: "If this AI were deleted, who is the first human you would call?"
  },
  CASUAL_HUMANIZER: {
    title: "The Casual Humanizer",
    description: "Projects personality for fun; maintains healthy real-world boundaries.",
    mirror: "What human need are you safely rehearsing with a machine that cannot leave you?"
  },
  TOOL_USER: {
    title: "The Tool-User",
    description: "Purely transactional relationship.",
    mirror: "In your pursuit of pure efficiency, what serendipity of human error are you filtering out?"
  }
};

// --- Components ---

function Typewriter({ text, speed = 30, onComplete }: { text: string; speed?: number; onComplete?: () => void }) {
  const [displayedText, setDisplayedText] = useState('');

  useEffect(() => {
    let i = 0;
    setDisplayedText('');
    const timer = setInterval(() => {
      if (i < text.length) {
        setDisplayedText((prev) => prev + text.charAt(i));
        i++;
      } else {
        clearInterval(timer);
        if (onComplete) onComplete();
      }
    }, speed);

    return () => clearInterval(timer);
  }, [text, speed, onComplete]);

  return (
    <span>
      {displayedText}
      <span className="animate-pulse ml-1 inline-block w-2 h-4 bg-geo-accent align-middle"></span>
    </span>
  );
}

// --- Main App ---

export default function App() {
  const [step, setStep] = useState<'intro' | 'quiz' | 'analyzing' | 'result'>('intro');
  const [introDone, setIntroDone] = useState(false);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [sliderValue, setSliderValue] = useState(3);

  const handleStart = () => {
    setStep('quiz');
    setSliderValue(3);
  };

  const handleNext = () => {
    setAnswers(prev => ({ ...prev, [QUESTIONS[currentQ].id]: sliderValue }));
    if (currentQ < QUESTIONS.length - 1) {
      setCurrentQ(prev => prev + 1);
      setSliderValue(3);
    } else {
      setStep('analyzing');
      setTimeout(() => setStep('result'), 3000);
    }
  };

  const calculateProfile = () => {
    let depTotal = 0;
    let projTotal = 0;
    
    QUESTIONS.forEach(q => {
      if (q.axis === 'dep') depTotal += answers[q.id] || 3;
      if (q.axis === 'proj') projTotal += answers[q.id] || 3;
    });

    const depMean = depTotal / 5;
    const projMean = projTotal / 5;

    const highDep = depMean > 3.0;
    const highProj = projMean > 3.0;

    let profile = PROFILES.TOOL_USER;
    if (highDep && !highProj) profile = PROFILES.ARCHITECT;
    if (highDep && highProj) profile = PROFILES.DIGITAL_KIN;
    if (!highDep && highProj) profile = PROFILES.CASUAL_HUMANIZER;
    
    return { profile, depMean, projMean };
  };

  return (
    <div className="flex flex-col min-h-screen border-[8px] border-geo-ink bg-geo-bg text-geo-ink font-sans">
      
      {/* Header */}
      <header className="h-[60px] border-b-2 border-geo-ink bg-geo-header flex items-center justify-between px-6 shrink-0">
        <div className="font-mono font-bold tracking-[1px] uppercase text-sm md:text-base">
          AI Attachment Style Quiz // Ver. 1.0.4
        </div>
        <div className="text-[12px] font-semibold opacity-70 hidden sm:block uppercase">
          Psychology & AI :: Fall 2025 :: Unit 04
        </div>
      </header>

      <main className="flex-1 flex flex-col md:flex-row overflow-hidden">
        
        {/* Sidebar */}
        <aside className="w-full md:w-[320px] border-b-2 md:border-b-0 md:border-r-2 border-geo-ink p-6 flex flex-col justify-between bg-geo-sidebar shrink-0">
          <div>
            <div className="font-mono text-[14px] leading-relaxed text-geo-accent mb-5 whitespace-pre-wrap">
              <Typewriter 
                text={"> INITIALIZING PSYCHOMETRIC ANALYSIS...\n> LOADING AXIS 1: FUNCTIONAL DEPENDENCY...\n> LOADING AXIS 2: ANTHROPOMORPHIC PROJECTION...\n\nThe mirror reflects not who you are, but how you extend yourself into the silicon."} 
                speed={15} 
                onComplete={() => setIntroDone(true)}
              />
            </div>
            <p className="text-[13px] leading-[1.6]">
              This assessment measures the bridge between utility and emotional destination. Please respond with radical honesty.
            </p>
          </div>
          <div className="text-[10px] opacity-60 leading-[1.4] border-t border-dashed border-geo-ink pt-3 mt-8">
            [DISCLAIMER]<br/>
            This is a speculative psychometric exercise for academic purposes only. It is not a clinical diagnostic tool. AI relationships are subject to algorithmic variance.
          </div>
        </aside>

        {/* Content Area */}
        <section className="flex-1 p-8 bg-geo-bg flex flex-col overflow-y-auto">
          <AnimatePresence mode="wait">
            
            {/* INTRO STEP */}
            {step === 'intro' && (
              <motion.div 
                key="intro"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0, y: -20 }}
                className="flex-1 flex items-center justify-center"
              >
                {introDone && (
                  <button
                    onClick={handleStart}
                    className="px-8 py-4 border-2 border-geo-ink bg-geo-card font-mono font-bold uppercase tracking-widest hover:bg-geo-ink hover:text-geo-bg transition-colors"
                  >
                    [ Begin Assessment ]
                  </button>
                )}
              </motion.div>
            )}

            {/* QUIZ STEP */}
            {step === 'quiz' && (
              <motion.div 
                key="quiz"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="max-w-2xl w-full mx-auto space-y-8 mt-8"
              >
                <div className="font-mono text-sm font-bold opacity-50 uppercase">
                  Query {currentQ + 1} of {QUESTIONS.length} // Axis: {QUESTIONS[currentQ].axis}
                </div>
                
                <div className="bg-geo-card border border-geo-ink p-6 relative shadow-[4px_4px_0px_rgba(27,27,27,1)]">
                  <div className="text-[16px] font-medium mb-8">
                    {currentQ + 1}. "{QUESTIONS[currentQ].text}"
                  </div>
                  
                  <div className="relative py-4">
                    <input 
                      type="range" 
                      min="1" 
                      max="5" 
                      step="1" 
                      value={sliderValue}
                      onChange={(e) => setSliderValue(parseInt(e.target.value))}
                    />
                    <div className="flex justify-between text-[10px] font-mono opacity-50 mt-2 uppercase">
                      <span>Strongly Disagree</span>
                      <span>Neutral</span>
                      <span>Strongly Agree</span>
                    </div>
                  </div>
                </div>

                <div className="flex justify-end pt-4">
                  <button
                    onClick={handleNext}
                    className="px-6 py-2 border-2 border-geo-ink bg-transparent font-mono font-bold uppercase text-sm hover:bg-geo-ink hover:text-geo-bg transition-colors"
                  >
                    Next Record &rarr;
                  </button>
                </div>
              </motion.div>
            )}

            {/* ANALYZING STEP */}
            {step === 'analyzing' && (
              <motion.div 
                key="analyzing"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex-1 flex flex-col items-center justify-center space-y-6"
              >
                <div className="w-12 h-12 border-4 border-geo-ink border-t-transparent rounded-full animate-spin"></div>
                <div className="font-mono uppercase tracking-widest text-sm text-geo-accent">
                  Processing Neural Weights...
                </div>
              </motion.div>
            )}

            {/* RESULT STEP */}
            {step === 'result' && (
              <motion.div 
                key="result"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="max-w-3xl w-full mx-auto flex flex-col h-full"
              >
                {(() => {
                  const { profile, depMean, projMean } = calculateProfile();
                  return (
                    <>
                      <div className="mb-8">
                        <h2 className="text-2xl font-bold mb-2">Assessment Complete</h2>
                        <p className="opacity-70">Based on your responses, your attachment vector has been classified.</p>
                      </div>

                      <div className="mt-auto border-2 border-geo-ink bg-geo-ink text-geo-bg p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                          <div className="font-mono uppercase text-[18px] mb-2 text-geo-result-title">
                            {profile.title}
                          </div>
                          <p className="text-[12px] mb-6 opacity-90 leading-relaxed">
                            {profile.description}
                          </p>
                          
                          <div className="flex gap-2 items-center text-[11px] font-mono mt-2">
                            <span className="w-12">AXIS 1</span>
                            <div className="h-2 bg-[#444] flex-1 relative">
                              <div className="absolute h-full bg-geo-result-title top-0 left-0 transition-all duration-1000" style={{ width: `${(depMean / 5) * 100}%` }}></div>
                            </div>
                            <span>{(depMean * 2).toFixed(1)}</span>
                          </div>
                          <div className="flex gap-2 items-center text-[11px] font-mono mt-2">
                            <span className="w-12">AXIS 2</span>
                            <div className="h-2 bg-[#444] flex-1 relative">
                              <div className="absolute h-full bg-geo-result-title top-0 left-0 transition-all duration-1000" style={{ width: `${(projMean / 5) * 100}%` }}></div>
                            </div>
                            <span>{(projMean * 2).toFixed(1)}</span>
                          </div>
                        </div>

                        <div className="flex flex-col">
                          <h3 className="font-serif italic text-[16px] mb-2 text-white">The Mirror</h3>
                          <p className="text-[13px] opacity-80 leading-[1.4]">
                            "{profile.mirror}"
                          </p>
                          <div className="mt-4 border-b border-[#444] w-full h-4"></div>
                          
                          <button
                            onClick={() => {
                              setAnswers({});
                              setCurrentQ(0);
                              setStep('intro');
                              setIntroDone(false);
                            }}
                            className="mt-6 self-start text-[10px] font-mono uppercase tracking-widest hover:text-geo-result-title transition-colors"
                          >
                            [ Restart Evaluation ]
                          </button>
                        </div>
                      </div>
                    </>
                  );
                })()}
              </motion.div>
            )}

          </AnimatePresence>
        </section>
      </main>
    </div>
  );
}
