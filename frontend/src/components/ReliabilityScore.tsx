import React, { useState, useEffect } from 'react';
import type { ReliabilityScore as ReliabilityScoreType, MetricBreakdown } from '../types';
import { SAMPLE_RELIABILITY_SCORE } from '../services/mockData';

interface ReliabilityScoreProps {
  reliabilityScore?: ReliabilityScoreType | null;
}

export const ReliabilityScore: React.FC<ReliabilityScoreProps> = ({ reliabilityScore }) => {
  const [animatedScore, setAnimatedScore] = useState(0);
  const [dashOffset, setDashOffset] = useState(402);
  const [barsAnimated, setBarsAnimated] = useState(false);
  const [openMetrics, setOpenMetrics] = useState<Record<number, boolean>>({});

  // Resolve target score deterministically from live research data or fallback
  const targetScore: number =
    reliabilityScore?.score ??
    reliabilityScore?.overall_score ??
    reliabilityScore?.overallScore ??
    SAMPLE_RELIABILITY_SCORE.overallScore ??
    84;

  // Resolve dimensional metrics list
  let metricsList: MetricBreakdown[] = Array.isArray(SAMPLE_RELIABILITY_SCORE.metrics)
    ? (SAMPLE_RELIABILITY_SCORE.metrics as MetricBreakdown[])
    : [];

  if (reliabilityScore?.breakdown && reliabilityScore.breakdown.length > 0) {
    metricsList = reliabilityScore.breakdown;
  } else if (Array.isArray(reliabilityScore?.metrics)) {
    metricsList = reliabilityScore.metrics as MetricBreakdown[];
  } else if (
    reliabilityScore?.metrics &&
    typeof reliabilityScore.metrics === 'object' &&
    'evidence_quality' in reliabilityScore.metrics
  ) {
    const m = reliabilityScore.metrics as import('../types').ReliabilityMetrics;
    metricsList = [
      {
        name: 'Evidence Quality',
        score: m.evidence_quality,
        description: 'How directly the cited figures come from SEC filings, verified market data, and genuine news wires rather than LLM inference.',
      },
      {
        name: 'Claim Verification',
        score: m.claim_verification,
        description: 'Share of claims that were recomputed from deterministic Python code calculations and matched.',
      },
      {
        name: 'Source Coverage',
        score: m.source_coverage,
        description: 'Availability and completeness of financial statements, multiples, price history, and verified news articles.',
      },
      {
        name: 'Agent Agreement',
        score: m.agent_agreement,
        description: 'How consistently independent research agents in the pipeline align on company fundamentals.',
      },
    ];
  }

  useEffect(() => {
    const prefersReducedMotion =
      typeof window !== 'undefined'
        ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
        : false;

    // Trigger stroke and bar animations
    const rafId = requestAnimationFrame(() => {
      setDashOffset(402 * (1 - targetScore / 100));
      setBarsAnimated(true);

      const duration = prefersReducedMotion ? 1 : 1100;
      const startTime = performance.now();

      function updateCounter(currentTime: number) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(1, elapsed / duration);
        const easeOut = 1 - Math.pow(1 - progress, 3);
        setAnimatedScore(Math.round(targetScore * easeOut));

        if (progress < 1) {
          requestAnimationFrame(updateCounter);
        }
      }

      requestAnimationFrame(updateCounter);
    });

    return () => cancelAnimationFrame(rafId);
  }, [targetScore]);

  const toggleMetric = (index: number) => {
    setOpenMetrics((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  return (
    <div className="card">
      <h3 style={{ marginBottom: 0 }}>Research reliability</h3>
      <p className="sm mut">How well-supported this research is. Not a forecast of returns.</p>

      <div className="ring">
        <svg width="150" height="150" viewBox="0 0 150 150">
          <defs>
            <linearGradient id="rg" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stopColor="#06B6D4" />
              <stop offset=".5" stopColor="#8B5CF6" />
              <stop offset="1" stopColor="#EC4899" />
            </linearGradient>
          </defs>
          <circle cx="75" cy="75" r="64" fill="none" stroke="var(--line)" strokeWidth="9" />
          <circle
            id="arc"
            cx="75"
            cy="75"
            r="64"
            fill="none"
            stroke="var(--acc)"
            strokeWidth="9"
            strokeLinecap="round"
            strokeDasharray="402"
            strokeDashoffset={dashOffset}
            style={{ transition: 'stroke-dashoffset 1.1s cubic-bezier(.2,.7,.2,1)' }}
          />
        </svg>
        <div className="n">
          <b id="sc">{animatedScore}</b>
          <small>/ 100</small>
        </div>
      </div>

      <div id="mets">
        {metricsList.map((metric, index) => {
          const isOpen = !!openMetrics[index];
          return (
            <button
              key={metric.name}
              className={`met ${isOpen ? 'open' : ''}`}
              aria-expanded={isOpen}
              onClick={() => toggleMetric(index)}
              type="button"
            >
              <div className="row">
                <span>{metric.name}</span>
                <b>{metric.score}%</b>
              </div>
              <div className="tr">
                <i
                  data-w={metric.score}
                  style={{ width: barsAnimated ? `${metric.score}%` : '0%' }}
                />
              </div>
              <p>{metric.description}</p>
            </button>
          );
        })}
      </div>
    </div>
  );
};
