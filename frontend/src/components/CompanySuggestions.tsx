import React from 'react';
import { SUGGESTED_TICKERS } from '../services/mockData';

interface CompanySuggestionsProps {
  onSelectSuggestion: (ticker: string) => void;
}

export const CompanySuggestions: React.FC<CompanySuggestionsProps> = ({ onSelectSuggestion }) => {
  return (
    <div className="chips" id="ex">
      {SUGGESTED_TICKERS.map((item) => (
        <button
          key={item}
          className="chip"
          type="button"
          onClick={() => onSelectSuggestion(item)}
        >
          {item}
        </button>
      ))}
    </div>
  );
};
