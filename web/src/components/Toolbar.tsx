interface ToolbarProps {
  onRun: () => void;
  onClear: () => void;
  isExecuting: boolean;
  sessionId: string | null;
}

export function Toolbar({ onRun, onClear, isExecuting, sessionId }: ToolbarProps) {
  return (
    <div className="flex items-center gap-3 px-4 py-2 bg-gray-800 border-b border-gray-700">
      <div className="flex items-center gap-2">
        <span className="text-lg font-bold tracking-tight">
          <span className="text-white">Math</span>
          <span className="text-emerald-400">Lang</span>
        </span>
        <span className="text-[10px] text-gray-500 uppercase tracking-widest border border-gray-600 px-1.5 py-0.5 rounded">
          Playground
        </span>
      </div>

      <div className="flex-1" />

      {sessionId && (
        <div className="text-xs text-gray-500">
          Session: <span className="font-mono">{sessionId.slice(0, 8)}</span>
        </div>
      )}

      <button
        onClick={onRun}
        disabled={isExecuting}
        className="flex items-center gap-2 px-4 py-1.5 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white text-sm font-medium rounded transition-colors"
      >
        {isExecuting ? (
          <>
            <span className="animate-spin">⏳</span>
            Running...
          </>
        ) : (
          <>
            <span>▶</span>
            Run
            <span className="text-xs text-green-300 ml-1">(Ctrl+Enter)</span>
          </>
        )}
      </button>

      <button
        onClick={onClear}
        className="px-4 py-1.5 bg-gray-700 hover:bg-gray-600 text-white text-sm font-medium rounded transition-colors"
      >
        Clear Session
      </button>
    </div>
  );
}
