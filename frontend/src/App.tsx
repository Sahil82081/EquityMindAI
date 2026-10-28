import React, { useState, useCallback } from 'react';
import type { Company, ResearchResponseData } from './types';
import { LandingPage } from './pages/LandingPage';
import { ResearchWorkspace } from './pages/ResearchWorkspace';
import { useResearchSimulation } from './hooks/useResearchSimulation';
import { saveRecentSearch } from './services/companyService';
import { initiateResearch } from './services/researchService';

export const App: React.FC = () => {
  const [currentCompany, setCurrentCompany] = useState<Company | null>(null);
  const [researchData, setResearchData] = useState<ResearchResponseData | null>(null);
  const [view, setView] = useState<'landing' | 'workspace'>('landing');
  const [isLandingOut, setIsLandingOut] = useState(false);

  const {
    stage,
    agentStatuses,
    stepStatuses,
    startSimulation,
    resetSimulation,
  } = useResearchSimulation(currentCompany, researchData);

  const handleStartResearch = useCallback(
    (company: Company) => {
      saveRecentSearch(company);
      setCurrentCompany(company);
      setIsLandingOut(true);

      // Trigger live backend research and financial data retrieval
      initiateResearch(company)
        .then((res) => {
          if (res) {
            setResearchData(res);
          }
        })
        .catch((err) => {
          console.error('Research initiation error:', err);
        });

      const prefersReducedMotion =
        typeof window !== 'undefined'
          ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
          : false;
      const transitionDelay = prefersReducedMotion ? 0 : 300;

      setTimeout(() => {
        setView('workspace');
        window.scrollTo(0, 0);
        startSimulation();
      }, transitionDelay);
    },
    [startSimulation]
  );

  const handleNewTicker = useCallback(() => {
    resetSimulation();
    setView('landing');
    setIsLandingOut(false);
    setCurrentCompany(null);
    setResearchData(null);
    window.scrollTo(0, 0);
  }, [resetSimulation]);

  return (
    <>
      {view === 'landing' && (
        <LandingPage
          isOut={isLandingOut}
          onStartResearch={handleStartResearch}
        />
      )}

      {view === 'workspace' && (
        <ResearchWorkspace
          company={currentCompany}
          stage={stage}
          agentStatuses={agentStatuses}
          stepStatuses={stepStatuses}
          researchData={researchData}
          onNewTicker={handleNewTicker}
        />
      )}
    </>
  );
};

export default App;
