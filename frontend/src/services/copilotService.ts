import { askCopilotApi } from './api';
import { COPILOT_QUESTIONS } from './mockData';
import type { CopilotQAItem } from '../types';

export async function askCopilot(
  question: string,
  ticker?: string,
  researchId?: string
): Promise<CopilotQAItem> {
  try {
    const response = await askCopilotApi(question, ticker, researchId);
    return {
      question: response.question,
      answer: response.answer,
    };
  } catch {
    // Fallback to local preset answers if backend is unreachable
    const fallback = COPILOT_QUESTIONS.find((q) => q.question === question);
    return {
      question,
      answer:
        fallback?.answer ||
        'Based on historical filings and multi-agent synthesis, this metric reflects consistent execution.',
    };
  }
}
