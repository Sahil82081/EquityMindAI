import React, { useState } from 'react';
import { COPILOT_QUESTIONS } from '../services/mockData';
import { askCopilot } from '../services/copilotService';
import type { CopilotQAItem } from '../types';

interface ResearchCopilotProps {
  ticker?: string;
  researchId?: string;
}

export const ResearchCopilot: React.FC<ResearchCopilotProps> = ({ ticker, researchId }) => {
  const [currentQA, setCurrentQA] = useState<CopilotQAItem | null>(null);
  const [loadingQuestion, setLoadingQuestion] = useState<string | null>(null);

  const handleAskQuestion = async (questionText: string) => {
    setLoadingQuestion(questionText);
    try {
      const qaItem = await askCopilot(questionText, ticker, researchId);
      // Show ONLY the current question's answer (replaces previous answer)
      setCurrentQA(qaItem);
    } finally {
      setLoadingQuestion(null);
    }
  };

  return (
    <div className="card" style={{ marginTop: '16px' }}>
      <h3>Research Q&A</h3>
      <p className="sm mut" style={{ marginBottom: '8px' }}>
        Ask about this report. Answers are anchored to the evidence above.
      </p>

      <div id="qs">
        {COPILOT_QUESTIONS.map((item) => {
          const isSelected = currentQA?.question === item.question;
          const isLoading = loadingQuestion === item.question;
          return (
            <button
              key={item.question}
              className={`chip pill ${isSelected ? 'active' : ''}`}
              type="button"
              disabled={isLoading}
              onClick={() => handleAskQuestion(item.question)}
            >
              {isLoading ? 'Synthesizing…' : item.question}
            </button>
          );
        })}
      </div>

      <div id="qa" aria-live="polite">
        {currentQA && (
          <div key={currentQA.question} className="ans">
            <b>{currentQA.question}</b>
            <p>{currentQA.answer}</p>
            <p className="sm mut">Anchored to research evidence</p>
          </div>
        )}
      </div>
    </div>
  );
};
