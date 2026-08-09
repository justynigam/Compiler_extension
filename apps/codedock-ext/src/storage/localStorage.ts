export async function saveToStorage(key: string, value: string): Promise<void> {
  await chrome.storage.local.set({ [key]: value });
}

export async function getFromStorage(key: string): Promise<string | null> {
  const result = await chrome.storage.local.get(key);
  return result[key] ?? null;
}

export async function saveLanguage(language: string): Promise<void> {
  await chrome.storage.local.set({ language });
}

export async function getSavedLanguage(): Promise<string> {
  const result = await chrome.storage.local.get('language');
  return result.language || 'java';
}

export async function saveCode(language: string, code: string): Promise<void> {
  await chrome.storage.local.set({ [`code_${language}`]: code });
}

export async function getSavedCode(language: string): Promise<string> {
  const result = await chrome.storage.local.get(`code_${language}`);
  return result[`code_${language}`] || '';
}

export async function saveInput(input: string): Promise<void> {
  await chrome.storage.local.set({ input });
}

export async function getSavedInput(): Promise<string> {
  const result = await chrome.storage.local.get('input');
  return result.input || '';
}