import React from 'react';
import type { Company } from '../types';
import { useCompanySearch } from '../hooks/useCompanySearch';
import { CompanySearch } from '../components/CompanySearch';
import { CompanySuggestions } from '../components/CompanySuggestions';
import { SelectedCompany } from '../components/SelectedCompany';

interface LandingPageProps {
  isOut: boolean;
  onStartResearch: (company: Company) => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ isOut, onStartResearch }) => {
  const {
    query,
    isOpen,
    isSearching,
    results,
    activeIndex,
    headerText,
    isFuzzy,
    isEmpty,
    selectedCompany,
    inputRef,
    dropdownRef,
    handleInputChange,
    handleKeyDown,
    pickCompany,
    clearSelection,
    selectSuggested,
    close,
    triggerSearch,
  } = useCompanySearch();

  return (
    <section id="landing" className={isOut ? 'out' : ''}>
      <div style={{ maxWidth: '640px' }}>
        <h1>EquityMind AI</h1>
        <p className="sub">AI-powered equity research with evidence-backed reasoning.</p>

        <CompanySearch
          query={query}
          isOpen={isOpen}
          isSearching={isSearching}
          results={results}
          activeIndex={activeIndex}
          headerText={headerText}
          isFuzzy={isFuzzy}
          isEmpty={isEmpty}
          inputRef={inputRef}
          dropdownRef={dropdownRef}
          onInputChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onFocus={() => {
            if (!selectedCompany) {
              triggerSearch(query);
            }
          }}
          onSelectCompany={pickCompany}
          onClose={close}
        />

        <CompanySuggestions onSelectSuggestion={selectSuggested} />

        <SelectedCompany
          company={selectedCompany}
          onChangeCompany={clearSelection}
          onStartResearch={onStartResearch}
        />

        <p className="note">
          Design preview. Every figure below is sample data for layout review and is not market
          data. In your app, <code>services/api</code> supplies live values.
        </p>
      </div>
    </section>
  );
};
