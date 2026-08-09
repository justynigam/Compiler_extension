import { useState, useEffect, useCallback } from 'react';
import LanguageSelector from '../components/LanguageSelector/LanguageSelector';
import CodeEditor from '../components/Editor/Editor';
import Console from '../components/Console/Console';
import Toolbar from '../components/Toolbar/Toolbar';
import Stats from '../components/Stats/Stats';
import { runCode } from '../services/api';
import {
  getSavedCode,
  getSavedInput,
  getSavedLanguage,
  saveCode,
  saveInput,
  saveLanguage,
} from '../storage/localStorage';

function getBoilerplateCode(lang: string): string {
  switch (lang) {
    case 'java':
      return `public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, CodeDock!");
    }
}`;
    case 'python':
      return `print("Hello, CodeDock!")`;
    case 'c':
      return `#include <stdio.h>

int main() {
    printf("Hello, CodeDock!\\n");
    return 0;
}`;
    case 'cpp':
      return `#include <iostream>

int main() {
    std::cout << "Hello, CodeDock!" << std::endl;
    return 0;
}`;
    case 'javascript':
      return `console.log("Hello, CodeDock!");`;
    default:
      return '';
  }
}

function getDownloadFilename(lang: string): string {
  switch (lang) {
    case 'java':
      return 'Main.java';
    case 'python':
      return 'program.py';
    case 'c':
      return 'program.c';
    case 'cpp':
      return 'program.cpp';
    case 'javascript':
      return 'program.js';
    default:
      return 'program.txt';
  }
}

function SidePanel() {
  const [language, setLanguage] = useState<string>('');
  const [code, setCode] = useState<string>('');
  const [input, setInput] = useState<string>('');
  const [output, setOutput] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [executionTime, setExecutionTime] = useState<number | null>(null);
  const [memory, setMemory] = useState<number | null>(null);
  const [exitCode, setExitCode] = useState<number | null>(null);
  const [hasRun, setHasRun] = useState<boolean>(false);

  useEffect(() => {
    getSavedLanguage().then((savedLang) => {
      const lang = savedLang || 'java';
      setLanguage(lang);
      getSavedCode(lang).then((savedCode) => {
        setCode(savedCode || getBoilerplateCode(lang));
      });
      getSavedInput().then((savedInput) => {
        setInput(savedInput || '');
      });
    });
  }, []);

  useEffect(() => {
    if (language) {
      saveLanguage(language);
    }
  }, [language]);

  useEffect(() => {
    if (language && code) {
      saveCode(language, code);
    }
  }, [code, language]);

  useEffect(() => {
    saveInput(input);
  }, [input]);

  const handleLanguageChange = useCallback(async (lang: string) => {
    setLanguage(lang);
    const savedCode = await getSavedCode(lang);
    setCode(savedCode || getBoilerplateCode(lang));
    setOutput('');
    setError('');
    setHasRun(false);
    setExecutionTime(null);
    setMemory(null);
    setExitCode(null);
  }, []);

  const handleRun = useCallback(async () => {
    if (isRunning) return;
    setIsRunning(true);
    setOutput('');
    setError('');
    setHasRun(false);

    try {
      const response = await runCode({ language, code, input });
      setOutput(response.output || '');
      setError(response.error || '');
      setExecutionTime(response.executionTime);
      setMemory(response.memory);
      setExitCode(response.exitCode);
      setHasRun(true);
    } catch (err: unknown) {
      const message =
        err instanceof Error
          ? err.message
          : 'Failed to connect to compiler service';
      setError(message);
      setHasRun(true);
    } finally {
      setIsRunning(false);
    }
  }, [isRunning, language, code, input]);

  const handleStop = useCallback(() => {
    setIsRunning(false);
  }, []);

  const handleClear = useCallback(() => {
    setOutput('');
    setError('');
    setInput('');
    setHasRun(false);
    setExecutionTime(null);
    setMemory(null);
    setExitCode(null);
  }, []);

  const handleDownload = useCallback(() => {
    const filename = getDownloadFilename(language);
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, [code, language]);

  if (!language) {
    return (
      <div className="flex items-center justify-center h-full text-gray-400">
        Loading...
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <LanguageSelector language={language} onLanguageChange={handleLanguageChange} />
      <div className="flex-1 min-h-0">
        <CodeEditor
          language={language}
          code={code}
          onChange={(value) => setCode(value || '')}
        />
      </div>
      <div className="flex flex-col gap-2 p-3 bg-gray-900 border-t border-gray-700">
        <Console
          type="input"
          label="INPUT"
          value={input}
          onChange={(val) => setInput(val)}
          readOnly={false}
        />
        <Console type="output" label="OUTPUT" value={output} readOnly />
        <Console type="error" label="ERROR" value={error} readOnly />
      </div>
      <Toolbar
        onRun={handleRun}
        onStop={handleStop}
        onClear={handleClear}
        onDownload={handleDownload}
        isRunning={isRunning}
      />
      <Stats
        executionTime={executionTime}
        memory={memory}
        exitCode={exitCode}
        language={language}
        visible={hasRun}
      />
    </div>
  );
}

export default SidePanel;