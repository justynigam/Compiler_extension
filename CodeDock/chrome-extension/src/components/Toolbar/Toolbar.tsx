import React from 'react';

interface ToolbarProps {
  onRun: () => void;
  onStop: () => void;
  onClear: () => void;
  onDownload: () => void;
  isRunning: boolean;
}

const Toolbar: React.FC<ToolbarProps> = ({
  onRun,
  onStop,
  onClear,
  onDownload,
  isRunning,
}) => {
  return (
    <div className="flex flex-row gap-2 px-3 py-2 border-t border-gray-700 bg-gray-800">
      <button
        onClick={onRun}
        disabled={isRunning}
        className="flex items-center gap-1 px-4 py-1.5 text-sm font-medium rounded-md bg-green-600 text-white hover:bg-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        ▶ Run
      </button>
      <button
        onClick={onStop}
        disabled={!isRunning}
        className="flex items-center gap-1 px-4 py-1.5 text-sm font-medium rounded-md bg-red-600 text-white hover:bg-red-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        ■ Stop
      </button>
      <button
        onClick={onClear}
        className="flex items-center gap-1 px-4 py-1.5 text-sm font-medium rounded-md bg-gray-600 text-white hover:bg-gray-500 transition-colors"
      >
        🗑 Clear
      </button>
      <button
        onClick={onDownload}
        className="flex items-center gap-1 px-4 py-1.5 text-sm font-medium rounded-md bg-blue-600 text-white hover:bg-blue-500 transition-colors"
      >
        ⬇ Download
      </button>
    </div>
  );
};

export default Toolbar;