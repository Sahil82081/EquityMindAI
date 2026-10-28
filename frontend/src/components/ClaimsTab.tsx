import React, { useState } from 'react';
import type { Claim } from '../types';
import { SAMPLE_CLAIMS } from '../services/mockData';

const STATUS_MAP: Record<string, { label: string; badgeClass: string }> = {
  ok: { label: '✓ Verified', badgeClass: 'b-ok' },
  warn: { label: '⚠ Partially verified', badgeClass: 'b-warn' },
  bad: { label: '✕ Unsupported', badgeClass: 'b-bad' },
  Verified: { label: '✓ Verified', badgeClass: 'b-ok' },
  'Partially Verified': { label: '⚠ Partially verified', badgeClass: 'b-warn' },
  Unsupported: { label: '✕ Unsupported', badgeClass: 'b-bad' },
  verified: { label: '✓ Verified', badgeClass: 'b-ok' },
  'partially verified': { label: '⚠ Partially verified', badgeClass: 'b-warn' },
  unsupported: { label: '✕ Unsupported', badgeClass: 'b-bad' },
};

interface ClaimsTabProps {
  claims?: Claim[] | null;
}

export const ClaimsTab: React.FC<ClaimsTabProps> = ({ claims: liveClaims }) => {
  const activeClaims = liveClaims && liveClaims.length > 0 ? liveClaims : SAMPLE_CLAIMS;

  const [openClaims, setOpenClaims] = useState<Record<number, boolean>>({
    0: true, // First claim open by default
  });

  const toggleClaim = (index: number) => {
    setOpenClaims((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  return (
    <div className="pane on" id="p-claims" role="tabpanel">
      <p className="sm mut">
        Each claim is linked to source data and a recomputed calculation. Select a claim to see the
        chain.
      </p>

      {activeClaims.map((claim, index) => {
        const isOpen = !!openClaims[index];
        const statusMeta = STATUS_MAP[claim.status] || STATUS_MAP.warn;

        return (
          <div key={index} className={`cl ${isOpen ? 'open' : ''}`}>
            <button
              type="button"
              aria-expanded={isOpen}
              onClick={() => toggleClaim(index)}
            >
              <span className="chev">▸</span>
              <span className="t">{claim.statement}</span>
              <span className={`badge ${statusMeta.badgeClass}`}>{statusMeta.label}</span>
            </button>

            <div className="bd">
              <div>
                <div className="chain">
                  <div className="st">
                    <small>Claim</small>
                    {claim.statement}
                  </div>
                  {claim.proofs.map((proof, pIdx) => (
                    <div key={pIdx} className="st code">
                      <small>{proof.label}</small>
                      {proof.detail}
                    </div>
                  ))}
                  <div className="st">
                    <small>Result</small>
                    {claim.result}
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
