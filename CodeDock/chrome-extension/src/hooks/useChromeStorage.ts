import { useState, useEffect, useCallback } from 'react';

export function useChromeStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T) => Promise<void>] {
  const [value, setInternalValue] = useState<T>(initialValue);

  useEffect(() => {
    chrome.storage.local.get(key).then((result) => {
      if (result[key] !== undefined) {
        setInternalValue(result[key] as T);
      }
    });
  }, [key]);

  const setValue = useCallback(
    async (newValue: T) => {
      setInternalValue(newValue);
      await chrome.storage.local.set({ [key]: newValue });
    },
    [key]
  );

  return [value, setValue];
}