import { useRef, useEffect } from 'react';
import type { DisplayResult } from '../types';

interface ResultsPanelProps {
  results: DisplayResult[];
  onClear: () => void;
}

export function ResultsPanel({ results, onClear }: ResultsPanelProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [results]);

  return (
    <div className="h-full flex flex-col bg-gray-900 rounded border border-gray-700">
      <div className="flex items-center justify-between px-3 py-2 border-b border-gray-700 bg-gray-800">
        <span className="text-sm font-medium text-gray-300">Results</span>
        {results.length > 0 && (
          <button
            onClick={onClear}
            className="text-xs text-gray-400 hover:text-white px-2 py-1 rounded hover:bg-gray-700"
          >
            Clear
          </button>
        )}
      </div>
      <div
        ref={containerRef}
        className="flex-1 overflow-y-auto p-2 space-y-2 font-mono text-sm"
      >
        {results.length === 0 ? (
          <div className="text-gray-500 text-center py-8">
            No results yet. Enter an expression and press Ctrl+Enter to evaluate.
          </div>
        ) : (
          results.map((result) => (
            <ResultItem key={result.id} result={result} />
          ))
        )}
      </div>
    </div>
  );
}

function ResultItem({ result }: { result: DisplayResult }) {
  const bgColor = result.isError ? 'bg-red-900/30' : 'bg-gray-800/50';
  const borderColor = result.isError ? 'border-red-700' : 'border-gray-700';

  return (
    <div className={`rounded border ${borderColor} ${bgColor} p-2`}>
      {result.isAssignment && result.variableName && (
        <div className="text-blue-400 text-xs mb-1">
          {result.variableName} =
        </div>
      )}
      {result.imageData ? (
        <div className="my-2">
          <img
            src={result.imageData}
            alt={result.output}
            className="max-w-full rounded"
          />
        </div>
      ) : (
        <div className={`${result.isError ? 'text-red-400' : 'text-green-400'}`}>
          {result.output}
        </div>
      )}
      <div className="text-gray-500 text-xs mt-1">
        {result.type}
      </div>
    </div>
  );
}
