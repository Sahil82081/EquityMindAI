import React, { useEffect, useRef } from 'react';
import type { Company } from '../types';
import { HighlightMatch } from '../utils/formatters';

interface CompanySearchProps {
  query: string;
  isOpen: boolean;
  isSearching: boolean;
  results: Company[];
  activeIndex: number;
  headerText: string | null;
  isFuzzy: boolean;
  isEmpty: boolean;
  inputRef: React.RefObject<HTMLInputElement | null>;
  dropdownRef: React.RefObject<HTMLDivElement | null>;
  onInputChange: (value: string) => void;
  onKeyDown: (e: React.KeyboardEvent<HTMLInputElement>) => void;
  onFocus: () => void;
  onSelectCompany: (company: Company) => void;
  onClose: () => void;
}

export const CompanySearch: React.FC<CompanySearchProps> = ({
  query,
  isOpen,
  isSearching,
  results,
  activeIndex,
  headerText,
  isFuzzy,
  isEmpty,
  inputRef,
  dropdownRef,
  onInputChange,
  onKeyDown,
  onFocus,
  onSelectCompany,
  onClose,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleDocumentClick = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        onClose();
      }
    };
    document.addEventListener('click', handleDocumentClick);
    return () => {
      document.removeEventListener('click', handleDocumentClick);
    };
  }, [onClose]);

  return (
    <div className="sb" id="sbw" ref={containerRef}>
      <div className="tick">
        <span className="ic" aria-hidden="true">
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          >
            <circle cx="11" cy="11" r="7" />
            <path d="M20 20l-3.5-3.5" />
          </svg>
        </span>
        <input
          id="t"
          ref={inputRef}
          role="combobox"
          aria-label="Search company or ticker"
          aria-expanded={isOpen}
          aria-controls="dd"
          aria-autocomplete="list"
          aria-activedescendant={activeIndex >= 0 ? `o${activeIndex}` : undefined}
          placeholder="Search company or ticker…"
          autoComplete="off"
          spellCheck={false}
          value={query}
          onChange={(e) => onInputChange(e.target.value)}
          onKeyDown={onKeyDown}
          onFocus={onFocus}
        />
        <span className={`spin ${isSearching ? 'on' : ''}`} id="sp" />
      </div>

      <div
        className={`dd ${isOpen ? 'show' : ''}`}
        id="dd"
        ref={dropdownRef}
        role="listbox"
        hidden={!isOpen}
      >
        {headerText && <div className="dh">{headerText}</div>}

        {isEmpty && (
          <div className="empty">
            <b>No company found</b>
            <p>Try searching by company name or ticker.</p>
          </div>
        )}

        {results.map((c, index) => {
          const isSelected = index === activeIndex;
          const highlightQuery = isFuzzy ? '' : query;

          return (
            <div
              key={`${c.ticker}-${index}`}
              className="opt"
              role="option"
              id={`o${index}`}
              aria-selected={isSelected}
              onMouseDown={(e) => {
                e.preventDefault();
                onSelectCompany(c);
              }}
            >
              <div className="oh">
                <b>
                  <HighlightMatch text={c.name} query={highlightQuery} />
                </b>
                <span className="badge b-n">
                  <HighlightMatch text={c.ticker} query={highlightQuery} />
                </span>
              </div>
              <div className="os">
                {c.exchange} · {c.market} · {c.sector}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
