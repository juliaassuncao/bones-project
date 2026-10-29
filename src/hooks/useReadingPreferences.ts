import { useCallback, useState } from 'react';
import type { ReadingPreferences } from '../types/content';
const KEY = 'bones:reading-preferences:v1';
const defaultPrefs: ReadingPreferences = { theme: 'paper', font: 'serif', size: 19, lineHeight: 1.85 };
function initial(): ReadingPreferences {
  try {
    const obj = JSON.parse(localStorage.getItem(KEY) || 'null') as ReadingPreferences | null;
    return obj && ['paper', 'night'].includes(obj.theme) && ['serif', 'sans'].includes(obj.font)
      ? { theme: obj.theme, font: obj.font, size: Math.min(24, Math.max(16, Number(obj.size) || 19)), lineHeight: Math.min(2.15, Math.max(1.5, Number(obj.lineHeight) || 1.85)) }
      : defaultPrefs;
  } catch { return defaultPrefs; }
}
export function useReadingPreferences() {
  const [prefs, setPrefs] = useState<ReadingPreferences>(initial);
  const update = useCallback((patch: Partial<ReadingPreferences>) => {
    setPrefs(prev => { const next = { ...prev, ...patch }; try { localStorage.setItem(KEY, JSON.stringify(next)); } catch { /* armazenamento opcional */ } return next; });
  }, []);
  return { prefs, update };
}
