import { useEffect, useState, useCallback } from 'react';
import { useSessionStore } from './store/session';
import { Toolbar } from './components/Toolbar';
import { ScriptEditor } from './components/ScriptEditor';
import { ResultsPanel } from './components/ResultsPanel';
import { VariablesPanel } from './components/VariablesPanel';
import { OperationsTree } from './components/OperationsTree';

const EXAMPLE_CODE = `# MathLang Playground
# A mathematical expression language with first-class functions

# Define functions with elegant syntax
square(x) = x^2
hypotenuse(a, b) = Sqrt(a^2 + b^2)

# Recursion works naturally
factorial(n) = If(n <= 1, 1, n * factorial(n - 1))
fib(n) = If(n <= 1, n, fib(n-1) + fib(n-2))

# Try them out
factorial(6)
fib(10)
hypotenuse(3, 4)

# Functional programming with collections
data = Range(1, 11)
Sum(Map(data, square))
Filter(data, x -> x % 2 == 0)
Reduce(data, (acc, x) -> acc + x, 0)

# Statistics
Mean(data)
StdDev(data)

# Mathematical constants and trig
circleArea(r) = [[PI]] * r^2
circleArea(5)

# Visualize functions
Plot(x -> Sin(x) * x, -10, 10)
`;

function App() {
  const [code, setCode] = useState(EXAMPLE_CODE);
  const {
    sessionId,
    variables,
    results,
    operationsByCategory,
    isExecuting,
    error,
    initialize,
    evaluate,
    clearSession,
    clearResults,
  } = useSessionStore();

  useEffect(() => {
    initialize();
  }, [initialize]);

  const handleRun = useCallback(async (codeToRun?: string) => {
    const source = codeToRun ?? code;
    if (source.trim()) {
      await clearSession();
      evaluate(source);
    }
  }, [code, evaluate, clearSession]);

  const handleInsertOperation = useCallback((text: string) => {
    setCode((prev) => prev + text);
  }, []);

  const handleInsertVariable = useCallback((name: string) => {
    setCode((prev) => prev + name);
  }, []);

  if (!sessionId) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-900 text-white">
        {error ? (
          <div className="text-red-400">Error: {error}</div>
        ) : (
          <div className="text-gray-400">Connecting to server...</div>
        )}
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-gray-900 text-white">
      <Toolbar
        onRun={handleRun}
        onClear={clearSession}
        isExecuting={isExecuting}
        sessionId={sessionId}
      />

      {error && (
        <div className="px-4 py-2 bg-red-900/50 border-b border-red-700 text-red-300 text-sm">
          {error}
        </div>
      )}

      <div className="flex-1 flex min-h-0">
        <div className="border-r border-gray-700 flex-shrink-0" style={{ width: '384px' }}>
          <OperationsTree
            operationsByCategory={operationsByCategory}
            onInsert={handleInsertOperation}
          />
        </div>

        <div className="flex-1 flex flex-col min-w-0">
          <div className="h-1/2">
            <ScriptEditor
              value={code}
              onChange={setCode}
              onExecute={handleRun}
              disabled={isExecuting}
            />
          </div>

          <div className="h-1/2 border-t border-gray-700">
            <ResultsPanel results={results} onClear={clearResults} />
          </div>
        </div>

        <div className="border-l border-gray-700 flex-shrink-0" style={{ width: '384px' }}>
          <VariablesPanel
            variables={variables}
            onInsert={handleInsertVariable}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
