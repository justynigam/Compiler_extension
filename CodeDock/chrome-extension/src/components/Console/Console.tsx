import React from 'react';

interface ConsoleProps {
  type: 'input' | 'output' | 'error';
  label: string;
  value: string;
  onChange?: (val: string) => void;
  readOnly?: boolean;
}

const Console: React.FC<ConsoleProps> = ({
  type,
  label,
  value,
  onChange,
  readOnly = false,
}) => {
  const borderColorMap: Record<string, string> = {
    input: 'border-green-500',
    output: 'border-gray-400',
    error: 'border-red-500',
  };

  const labelColorMap: Record<string, string> = {
    input: 'text-green-400',
    output: 'text-gray-300',
    error: 'text-red-400',
  };

  return (
    <div className={`flex flex-col border ${borderColorMap[type]} rounded-md overflow-hidden`}>
      <div className={`px-3 py-1 text-xs font-semibold bg-gray-800 ${labelColorMap[type]}`}>
        {label}
      </div>
      {readOnly ? (
        <pre className="p-3 text-sm font-mono text-gray-300 bg-gray-900 whitespace-pre-wrap break-all overflow-auto max-h-32 min-h-[3rem] m-0">
          {value || (type === 'output' ? 'Ready' : '')}
        </pre>
      ) : (
        <textarea
          value={value}
          onChange={(e) => onChange?.(e.target.value)}
          placeholder="Enter input..."
          rows={3}
          className="bg-gray-900 text-gray-200 p-3 text-sm font-mono resize-none focus:outline-none placeholder-gray-500"
        />
      )}
    </div>
  );
};

export default Console;