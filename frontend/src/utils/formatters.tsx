import React from 'react';

interface HighlightMatchProps {
  text: string;
  query: string;
}

export const HighlightMatch: React.FC<HighlightMatchProps> = ({ text, query }) => {
  const q = query.trim().toLowerCase();
  if (!q) {
    return <>{text}</>;
  }

  const index = text.toLowerCase().indexOf(q);
  if (index === -1) {
    return <>{text}</>;
  }

  const before = text.slice(0, index);
  const match = text.slice(index, index + q.length);
  const after = text.slice(index + q.length);

  return (
    <>
      {before}
      <mark>{match}</mark>
      {after}
    </>
  );
};
