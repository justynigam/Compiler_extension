import React from 'react';

interface StatsProps {
  executionTime: number | null;
  memory: number | null;
  exitCode: number | null;
  language: string;
  visible: boolean;
}

const Stats: React.FC<StatsProps> = ({
  executionTime,
  memory,
  exitCode,
  language,
  visible,
}) => {
  if (!visible) {
    return null;
  }

  return (
    <div className="flex flex-row gap-4 px-3 py-1.5 text-xs text-gray-400 bg-gray-800 border-t border-gray-700 justify-start">
      <span>
        <span className="text-gray-500">Lang:</span> {language}
      </span>
      <span>
        <span className="text-gray-500">Time:</span>{' '}
        {executionTime !== null ? `${executionTime} ms` : '--'}
      </span>
      <span>
        <span className="text-gray-500">Memory:</span>{' '}
        {memory !== null ? `${memory} KB` : '--'}
      </span>
      <span>
        <span className="text-gray-500">Exit:</span>{' '}
        {exitCode !== null ? exitCode : '--'}
      </span>
    </div>
  );
};

export default Stats;