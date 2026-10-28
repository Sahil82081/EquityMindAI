import React, { useState } from 'react';
import { COPILOT_QUESTIONS } from '../services/mockData';
import { askCopilot } from '../services/copilotService';
import type { CopilotQAItem } from '../types';

interface ResearchCopilotProps {
  ticker?: string;
  researchId?: string;
}

export const ResearchCopilot: React.FC<ResearchCopilotProps> = ({ ticker, researchId }) => {
  const [history, setHistory] = useState<CopilotQAItem[]>([]);
  const [loadingQuestion, setLoadingQuestion] = useState<string | null>(null);

  const handleAskQuestion = async (questionText: string) => {
    setLoadingQuestion(questionText);
    try {
      const qaItem = await askCopilot(questionText, ticker, researchId);
      // Prepend new answer to the list, matching prototype's insertAdjacentHTML("afterbegin")
      setHistory((prev) => [qaItem, ...prev]);
    } finally {
      setLoadingQuestion(null);
    }
  };

  return (
    <div className="card" style={{ marginTop: '16px' }}>
      <h3>Research copilot</h3>
      <p className="sm mut" style={{ marginBottom: '8px' }}>
        Ask about this report. Answers are anchored to the evidence above.
      </p>

      <div id="qs">
        {COPILOT_QUESTIONS.map((item) => (
          <button
            key={item.question}
            className="chip pill"
            type="button"
            disabled={loadingQuestion === item.question}
            onClick={() => handleAskQuestion(item.question)}
          >
            {loadingQuestion === item.question ? 'Synthesizing…' : item.question}
          </button>
        ))}
      </div>

      <div id="qa" aria-live="polite">
        {history.map((item, idx) => (
          <div key={`${item.question}-${idx}`} className="ans">
            <b>{item.question}</b>
            <p>{item.answer}</p>
            <p className="sm mut">Anchored to research evidence</p>
          </div>
        ))}
      </div>
    </div>
  );
};
