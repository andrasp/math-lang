import { useState } from 'react';

interface VariablesPanelProps {
  variables: Record<string, { value: string; type: string }>;
  onInsert?: (name: string) => void;
}

export function VariablesPanel({ variables, onInsert }: VariablesPanelProps) {
  const [selectedVar, setSelectedVar] = useState<string | null>(null);
  const entries = Object.entries(variables);
  const selectedData = selectedVar ? variables[selectedVar] : null;

  return (
    <div className="h-full flex flex-col bg-gray-900 rounded border border-gray-700">
      <div className="flex-1 flex flex-col min-h-0 border-b border-gray-700">
        <div className="px-3 py-2 border-b border-gray-700 bg-gray-800">
          <span className="text-sm font-medium text-gray-300">Variables</span>
          <span className="text-xs text-gray-500 ml-2">({entries.length})</span>
        </div>
        <div className="flex-1 overflow-y-auto">
          {entries.length === 0 ? (
            <div className="text-gray-500 text-center py-4 text-sm">
              No variables defined
            </div>
          ) : (
            <table className="w-full text-sm">
              <thead className="bg-gray-800/50 sticky top-0">
                <tr className="text-gray-400 text-xs">
                  <th className="text-left px-3 py-1 font-normal">Name</th>
                  <th className="text-left px-3 py-1 font-normal">Type</th>
                </tr>
              </thead>
              <tbody>
                {entries.map(([name, { type }]) => (
                  <tr
                    key={name}
                    className={`border-t border-gray-800 hover:bg-gray-800/50 cursor-pointer ${
                      selectedVar === name ? 'bg-blue-900/30' : ''
                    }`}
                    onClick={() => setSelectedVar(name)}
                    onDoubleClick={() => onInsert?.(name)}
                    title="Click to view details, double-click to insert"
                  >
                    <td className="px-3 py-1 text-blue-400 font-mono">{name}</td>
                    <td className="px-3 py-1 text-gray-500">{type}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      <div className="flex-1 flex flex-col min-h-0">
        <div className="px-3 py-2 border-b border-gray-700 bg-gray-800 flex items-center justify-between">
          <span className="text-sm font-medium text-gray-300">
            {selectedVar ? selectedVar : 'Details'}
          </span>
          {selectedVar && (
            <button
              onClick={() => onInsert?.(selectedVar)}
              className="text-xs px-2 py-0.5 bg-blue-600 hover:bg-blue-500 text-white rounded"
              title="Insert into editor"
            >
              Insert
            </button>
          )}
        </div>
        <div className="flex-1 overflow-y-auto p-3">
          {selectedData ? (
            <div className="space-y-3">
              <div>
                <div className="text-xs text-gray-500 mb-1">Type</div>
                <div className="text-sm text-purple-400 font-mono">{selectedData.type}</div>
              </div>
              <div>
                <div className="text-xs text-gray-500 mb-1">Value</div>
                <pre className="text-sm text-green-400 font-mono whitespace-pre-wrap break-all bg-gray-800/50 p-2 rounded">
                  {selectedData.value}
                </pre>
              </div>
            </div>
          ) : (
            <div className="text-gray-500 text-center text-sm">
              Select a variable to view details
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
