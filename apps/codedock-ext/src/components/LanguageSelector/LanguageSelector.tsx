import React from 'react';

interface LanguageSelectorProps {
  language: string;
  onLanguageChange: (lang: string) => void;
}

const languages = [
  { value: 'java', label: 'Java' },
  { value: 'python', label: 'Python' },
  { value: 'c', label: 'C' },
  { value: 'cpp', label: 'C++' },
  { value: 'javascript', label: 'JavaScript' },
];

const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  language,
  onLanguageChange,
}) => {
  return (
    <div className="flex items-center gap-2 px-3 py-2 border-b border-gray-700 bg-gray-800">
      <label htmlFor="language-select" className="text-sm text-gray-400 font-medium">
        Language:
      </label>
      <select
        id="language-select"
        value={language}
        onChange={(e) => onLanguageChange(e.target.value)}
        className="bg-gray-700 text-gray-200 border border-gray-600 rounded-md px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-accent-blue cursor-pointer hover:bg-gray-600 transition-colors"
      >
        {languages.map((lang) => (
          <option key={lang.value} value={lang.value}>
            {lang.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSelector;