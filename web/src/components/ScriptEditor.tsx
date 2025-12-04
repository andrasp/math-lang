import { useRef, useCallback } from 'react';
import Editor, { type OnMount } from '@monaco-editor/react';
import type { editor } from 'monaco-editor';

interface ScriptEditorProps {
  value: string;
  onChange: (value: string) => void;
  onExecute: (code: string) => void;
  disabled?: boolean;
}

export function ScriptEditor({ value, onChange, onExecute, disabled }: ScriptEditorProps) {
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);
  const onExecuteRef = useRef(onExecute);
  onExecuteRef.current = onExecute;

  const handleEditorMount: OnMount = useCallback((editor, monaco) => {
    editorRef.current = editor;

    monaco.languages.register({ id: 'mathlang' });
    monaco.languages.setMonarchTokensProvider('mathlang', {
      keywords: ['def', 'if', 'else', 'then'],
      operators: ['+', '-', '*', '/', '^', '%', '=', '==', '!=', '<', '>', '<=', '>=', '->'],
      symbols: /[=><!~?:&|+\-*\/\^%]+/,

      tokenizer: {
        root: [
          [/#.*$/, 'comment'],
          [/\[\[[A-Z_][A-Z0-9_]*\]\]/, 'constant'],
          [/[A-Z][a-zA-Z0-9]*(?=\s*\()/, 'function'],
          [/"[^"]*"/, 'string'],
          [/\d+\.\d*([eE][+-]?\d+)?/, 'number.float'],
          [/\.\d+([eE][+-]?\d+)?/, 'number.float'],
          [/\d+[eE][+-]?\d+/, 'number.float'],
          [/0[xX][0-9a-fA-F]+/, 'number.hex'],
          [/\d+/, 'number'],
          [/\d+(\.\d+)?[ij]/, 'number'],
          [/[a-zA-Z_]\w*/, {
            cases: {
              '@keywords': 'keyword',
              '@default': 'identifier'
            }
          }],
          [/->/, 'operator'],
          [/@symbols/, 'operator'],
          [/[{}()\[\]]/, '@brackets'],
          [/[;,]/, 'delimiter'],
        ],
      }
    });

    monaco.editor.defineTheme('mathlang-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [
        { token: 'comment', foreground: '6A9955' },
        { token: 'constant', foreground: '4EC9B0', fontStyle: 'bold' },
        { token: 'function', foreground: 'DCDCAA' },
        { token: 'string', foreground: 'CE9178' },
        { token: 'number', foreground: 'B5CEA8' },
        { token: 'number.float', foreground: 'B5CEA8' },
        { token: 'number.hex', foreground: 'B5CEA8' },
        { token: 'keyword', foreground: 'C586C0' },
        { token: 'operator', foreground: 'D4D4D4' },
        { token: 'identifier', foreground: '9CDCFE' },
      ],
      colors: {
        'editor.background': '#1e1e1e',
      }
    });

    monaco.editor.setTheme('mathlang-dark');

    editor.addAction({
      id: 'execute-code',
      label: 'Execute Code',
      keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter],
      run: (ed) => {
        const currentCode = ed.getValue();
        onExecuteRef.current(currentCode);
      },
    });

  }, []);

  return (
    <div className="h-full w-full border border-gray-700 rounded overflow-hidden">
      <Editor
        height="100%"
        defaultLanguage="mathlang"
        value={value}
        onChange={(v) => onChange(v ?? '')}
        onMount={handleEditorMount}
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 2,
          wordWrap: 'on',
          readOnly: disabled,
        }}
      />
    </div>
  );
}
