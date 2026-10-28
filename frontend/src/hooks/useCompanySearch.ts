import { useState, useRef, useCallback } from 'react';
import type { Company } from '../types';
import { getRecentSearches, searchCompanies } from '../services/companyService';

export function useCompanySearch(onCompanySelected?: (company: Company) => void) {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [results, setResults] = useState<Company[]>([]);
  const [activeIndex, setActiveIndex] = useState(-1);
  const [headerText, setHeaderText] = useState<string | null>(null);
  const [isFuzzy, setIsFuzzy] = useState(false);
  const [isEmpty, setIsEmpty] = useState(false);
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);

  const tokenRef = useRef(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const prefersReducedMotion = typeof window !== 'undefined'
    ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
    : false;

  const close = useCallback(() => {
    setIsOpen(false);
    setActiveIndex(-1);
  }, []);

  const openWithResults = useCallback((list: Company[], header: string | null, fuzzy = false) => {
    setResults(list);
    setHeaderText(header);
    setIsFuzzy(fuzzy);
    setIsEmpty(false);
    setActiveIndex(-1);
    setIsOpen(true);
  }, []);

  const openEmpty = useCallback(() => {
    setResults([]);
    setHeaderText(null);
    setIsFuzzy(false);
    setIsEmpty(true);
    setActiveIndex(-1);
    setIsOpen(true);
  }, []);

  const triggerSearch = useCallback((searchTerm: string) => {
    setSelectedCompany(null);
    const trimmed = searchTerm.trim();

    if (!trimmed) {
      tokenRef.current++;
      setIsSearching(false);
      const recents = getRecentSearches();
      if (recents.length > 0) {
        openWithResults(recents, 'Recent searches', false);
      } else {
        close();
      }
      return;
    }

    const currentToken = ++tokenRef.current;
    setIsSearching(true);
    setIsOpen(true);
    setHeaderText('Searching…');
    setResults([]);
    setIsEmpty(false);

    const delay = prefersReducedMotion ? 0 : 220;
    setTimeout(async () => {
      if (currentToken !== tokenRef.current) return;

      const { results: resolvedResults, fuzzy } = await searchCompanies(searchTerm);
      if (currentToken !== tokenRef.current) return;
      setIsSearching(false);

      if (resolvedResults.length === 0) {
        openEmpty();
        return;
      }

      let header = '';
      if (fuzzy) {
        header = `Did you mean ${resolvedResults[0].name} (${resolvedResults[0].ticker})?`;
      } else if (resolvedResults.length > 1) {
        header = `${resolvedResults.length} companies match. Select one.`;
      }

      openWithResults(resolvedResults, header || null, fuzzy);
    }, delay);
  }, [close, openEmpty, openWithResults, prefersReducedMotion]);

  const handleInputChange = (val: string) => {
    setQuery(val);
    triggerSearch(val);
  };

  const pickCompany = useCallback((company: Company) => {
    tokenRef.current++;
    setIsSearching(false);
    setSelectedCompany(company);
    setQuery(company.name);
    close();
    onCompanySelected?.(company);
  }, [close, onCompanySelected]);

  const clearSelection = useCallback(() => {
    setSelectedCompany(null);
    tokenRef.current++;
    setQuery('');
    close();
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, [close]);

  const selectSuggested = useCallback((tickerOrName: string) => {
    setQuery(tickerOrName);
    if (inputRef.current) {
      inputRef.current.focus();
    }
    triggerSearch(tickerOrName);
  }, [triggerSearch]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    const total = results.length;
    const key = e.key;

    if (key === 'Escape') {
      close();
      return;
    }

    if (key === 'ArrowDown') {
      e.preventDefault();
      if (!isOpen && !selectedCompany) {
        triggerSearch(query);
        return;
      }
      if (total > 0) {
        setActiveIndex((prev) => (prev + 1) % total);
      }
    } else if (key === 'ArrowUp') {
      e.preventDefault();
      if (total > 0) {
        setActiveIndex((prev) => (prev - 1 + total) % total);
      }
    } else if (key === 'Enter') {
      e.preventDefault();
      if (selectedCompany) {
        return;
      }
      if (activeIndex >= 0 && results[activeIndex]) {
        pickCompany(results[activeIndex]);
        return;
      }
      if (total === 1) {
        pickCompany(results[0]);
        return;
      }
      if (total > 0) {
        setActiveIndex(0);
      }
    }
  };

  return {
    query,
    setQuery,
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
  };
}
