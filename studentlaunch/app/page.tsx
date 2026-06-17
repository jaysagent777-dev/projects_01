"use client";
import { useState } from "react";

const ROADMAP_STEPS = [
  {
    id: 1,
    title: "Define Your Problem",
    description: "Every great business solves a real problem. Write it in one sentence.",
    action: "Write your problem statement",
    tip: "Bad: 'I want to build an app.' Good: 'Students waste 2 hours/day searching for study resources.'",
  },
  {
    id: 2,
    title: "Validate the Problem",
    description: "Talk to 10 real people who have this problem before building anything.",
    action: "Interview 10 potential customers",
    tip: "Ask: 'Tell me about the last time you experienced this problem.' Listen, don't pitch.",
  },
  {
    id: 3,
    title: "Define Your Solution",
    description: "Describe your solution in one sentence. Keep it simple.",
    action: "Write your solution statement",
    tip: "If you can't explain it simply, it's too complex. Simplify.",
  },
  {
    id: 4,
    title: "Build a Landing Page",
    description: "Create a simple page describing your product before you build it.",
    action: "Launch a landing page with a waitlist",
    tip: "Use Carrd, Webflow, or Notion. Collect emails. 100 signups = real demand.",
  },
  {
    id: 5,
    title: "Get Your First 10 Customers",
    description: "Don't wait for perfection. Sell manually to your first 10 customers.",
    action: "Close 10 paying customers",
    tip: "Do things that don't scale. DM people. Do it by hand. Charge from day one.",
  },
  {
    id: 6,
    title: "Build the MVP",
    description: "Now build the minimum product that solves the problem for your 10 customers.",
    action: "Ship your MVP",
    tip: "MVP = fewest features needed to deliver value. Cut everything else.",
  },
  {
    id: 7,
    title: "Get Feedback & Iterate",
    description: "Talk to your customers weekly. Improve based on what they say.",
    action: "Run weekly feedback sessions",
    tip: "Ask: 'What would make you tell a friend about this?' Then build that.",
  },
  {
    id: 8,
    title: "Grow",
    description: "Find one channel that works and double down on it.",
    action: "Identify your growth channel",
    tip: "SEO, social, referrals, cold outreach — pick one and master it before adding more.",
  },
];

const VALIDATION_QUESTIONS = [
  "Who exactly has this problem? (Be specific — age, situation, location)",
  "How are they solving it today?",
  "What's wrong with their current solution?",
  "How often do they face this problem?",
  "Would they pay to solve it? How much?",
];

export default function Home() {
  const [activeTab, setActiveTab] = useState<"roadmap" | "validate" | "idea">("idea");
  const [idea, setIdea] = useState("");
  const [answers, setAnswers] = useState<string[]>(Array(VALIDATION_QUESTIONS.length).fill(""));
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);
  const [validationScore, setValidationScore] = useState<number | null>(null);

  const toggleStep = (id: number) => {
    setCompletedSteps((prev) =>
      prev.includes(id) ? prev.filter((s) => s !== id) : [...prev, id]
    );
  };

  const calculateScore = () => {
    const filled = answers.filter((a) => a.trim().length > 20).length;
    setValidationScore(Math.round((filled / VALIDATION_QUESTIONS.length) * 100));
    setActiveTab("validate");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      <header className="border-b border-white/10 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">StudentLaunch</h1>
            <p className="text-purple-300 text-sm">From idea to first customer</p>
          </div>
          <div className="flex gap-2">
            {(["idea", "validate", "roadmap"] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 rounded-lg text-sm font-medium capitalize transition-all ${
                  activeTab === tab
                    ? "bg-purple-600 text-white"
                    : "text-purple-300 hover:text-white hover:bg-white/10"
                }`}
              >
                {tab === "idea" ? "My Idea" : tab === "validate" ? "Validate" : "Roadmap"}
              </button>
            ))}
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-10">
        {activeTab === "idea" && (
          <div className="space-y-8">
            <div>
              <h2 className="text-3xl font-bold mb-2">What&apos;s your idea?</h2>
              <p className="text-purple-300">Describe it in one or two sentences. Don&apos;t overthink it.</p>
            </div>

            <textarea
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              placeholder="e.g. An app that helps college students find study groups based on their courses and schedule..."
              className="w-full h-40 bg-white/5 border border-white/10 rounded-xl p-4 text-white placeholder-white/30 focus:outline-none focus:border-purple-500 resize-none text-lg"
            />

            <div className="bg-white/5 border border-white/10 rounded-xl p-6 space-y-4">
              <h3 className="font-semibold text-purple-300 uppercase text-xs tracking-wider">Validate your idea</h3>
              <p className="text-white/80">Answer these 5 questions honestly. They&apos;ll tell you if your idea is worth pursuing.</p>
              {VALIDATION_QUESTIONS.map((q, i) => (
                <div key={i} className="space-y-2">
                  <label className="text-sm text-white/70">{i + 1}. {q}</label>
                  <textarea
                    value={answers[i]}
                    onChange={(e) => {
                      const updated = [...answers];
                      updated[i] = e.target.value;
                      setAnswers(updated);
                    }}
                    placeholder="Your answer..."
                    className="w-full h-20 bg-white/5 border border-white/10 rounded-lg p-3 text-white placeholder-white/30 focus:outline-none focus:border-purple-500 resize-none text-sm"
                  />
                </div>
              ))}
              <button
                onClick={calculateScore}
                disabled={!idea.trim()}
                className="w-full py-3 bg-purple-600 hover:bg-purple-500 disabled:opacity-40 disabled:cursor-not-allowed rounded-xl font-semibold transition-all"
              >
                Check My Validation Score →
              </button>
            </div>
          </div>
        )}

        {activeTab === "validate" && (
          <div className="space-y-8">
            <div>
              <h2 className="text-3xl font-bold mb-2">Validation Results</h2>
              <p className="text-purple-300">Here&apos;s how well-validated your idea is right now.</p>
            </div>

            {validationScore !== null ? (
              <div className="space-y-6">
                <div className="bg-white/5 border border-white/10 rounded-xl p-8 text-center">
                  <div className={`text-7xl font-bold mb-2 ${validationScore >= 80 ? "text-green-400" : validationScore >= 60 ? "text-yellow-400" : "text-red-400"}`}>
                    {validationScore}%
                  </div>
                  <p className="text-white/60 text-lg">
                    {validationScore >= 80
                      ? "Strong idea — move to roadmap"
                      : validationScore >= 60
                      ? "Getting there — answer more questions"
                      : "Needs more validation — talk to real people first"}
                  </p>
                </div>

                {idea && (
                  <div className="bg-white/5 border border-white/10 rounded-xl p-6">
                    <p className="text-purple-300 text-xs uppercase tracking-wider mb-2">Your Idea</p>
                    <p className="text-white">{idea}</p>
                  </div>
                )}

                <div className="space-y-3">
                  {VALIDATION_QUESTIONS.map((q, i) => (
                    <div key={i} className={`rounded-xl p-4 border ${answers[i].trim().length > 20 ? "bg-green-500/10 border-green-500/30" : "bg-red-500/10 border-red-500/30"}`}>
                      <p className="text-sm text-white/60 mb-1">{q}</p>
                      <p className="text-white text-sm">{answers[i] || "Not answered"}</p>
                    </div>
                  ))}
                </div>

                {validationScore >= 60 && (
                  <button
                    onClick={() => setActiveTab("roadmap")}
                    className="w-full py-3 bg-purple-600 hover:bg-purple-500 rounded-xl font-semibold transition-all"
                  >
                    See My Roadmap to First Customer →
                  </button>
                )}
              </div>
            ) : (
              <div className="text-center py-20 text-white/40">
                <p className="text-lg">No validation score yet.</p>
                <button onClick={() => setActiveTab("idea")} className="mt-4 text-purple-400 hover:text-purple-300 underline">
                  Go validate your idea first
                </button>
              </div>
            )}
          </div>
        )}

        {activeTab === "roadmap" && (
          <div className="space-y-8">
            <div>
              <h2 className="text-3xl font-bold mb-2">Your Roadmap</h2>
              <p className="text-purple-300">8 steps from idea to first paying customer. Check them off as you go.</p>
            </div>

            <div className="flex items-center gap-3 bg-white/5 border border-white/10 rounded-xl p-4">
              <div className="text-2xl font-bold text-purple-400">{completedSteps.length}/{ROADMAP_STEPS.length}</div>
              <div className="flex-1">
                <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-purple-500 rounded-full transition-all"
                    style={{ width: `${(completedSteps.length / ROADMAP_STEPS.length) * 100}%` }}
                  />
                </div>
                <p className="text-white/40 text-xs mt-1">steps completed</p>
              </div>
            </div>

            <div className="space-y-4">
              {ROADMAP_STEPS.map((step) => {
                const done = completedSteps.includes(step.id);
                return (
                  <div
                    key={step.id}
                    className={`rounded-xl border p-6 transition-all ${done ? "bg-purple-600/20 border-purple-500/40" : "bg-white/5 border-white/10"}`}
                  >
                    <div className="flex items-start gap-4">
                      <button
                        onClick={() => toggleStep(step.id)}
                        className={`mt-1 w-6 h-6 rounded-full border-2 flex-shrink-0 flex items-center justify-center transition-all ${done ? "bg-purple-500 border-purple-500" : "border-white/30 hover:border-purple-400"}`}
                      >
                        {done && <span className="text-white text-xs">✓</span>}
                      </button>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-purple-400 text-xs font-mono">STEP {step.id}</span>
                        </div>
                        <h3 className={`text-lg font-semibold mb-1 ${done ? "line-through text-white/50" : "text-white"}`}>
                          {step.title}
                        </h3>
                        <p className="text-white/60 text-sm mb-3">{step.description}</p>
                        <div className="bg-white/5 rounded-lg p-3">
                          <p className="text-xs text-purple-300 uppercase tracking-wider mb-1">Action</p>
                          <p className="text-sm text-white">{step.action}</p>
                        </div>
                        <div className="mt-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-3">
                          <p className="text-xs text-yellow-400 uppercase tracking-wider mb-1">Tip</p>
                          <p className="text-sm text-white/70">{step.tip}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
