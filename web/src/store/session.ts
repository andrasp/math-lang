import { create } from 'zustand';
import type { DisplayResult, Operation } from '../types';
import * as api from '../api/client';

interface SessionState {
  sessionId: string | null;
  variables: Record<string, { value: string; type: string }>;
  results: DisplayResult[];
  operations: Operation[];
  operationsByCategory: Record<string, Operation[]>;
  isExecuting: boolean;
  error: string | null;

  initialize: () => Promise<void>;
  evaluate: (source: string) => Promise<void>;
  clearSession: () => Promise<void>;
  clearResults: () => void;
}

let resultIdCounter = 0;

export const useSessionStore = create<SessionState>((set, get) => ({
  sessionId: null,
  variables: {},
  results: [],
  operations: [],
  operationsByCategory: {},
  isExecuting: false,
  error: null,

  initialize: async () => {
    try {
      const session = await api.createSession();
      const ops = await api.getOperations();

      const byCategory: Record<string, Operation[]> = {};
      for (const op of ops.operations) {
        if (!byCategory[op.category]) {
          byCategory[op.category] = [];
        }
        byCategory[op.category].push(op);
      }

      set({
        sessionId: session.session_id,
        variables: session.variables,
        operations: ops.operations,
        operationsByCategory: byCategory,
        error: null,
      });
    } catch (e) {
      set({ error: e instanceof Error ? e.message : 'Failed to initialize' });
    }
  },

  evaluate: async (source: string) => {
    const { sessionId } = get();
    if (!sessionId) {
      set({ error: 'No session' });
      return;
    }

    set({ isExecuting: true, error: null });

    try {
      const response = await api.evaluate({ source, session_id: sessionId });

      const newResults: DisplayResult[] = [];

      if (response.error) {
        newResults.push({
          id: `result-${++resultIdCounter}`,
          input: source,
          output: response.error.message,
          type: 'Error',
          isAssignment: false,
          variableName: null,
          isError: true,
          timestamp: new Date(),
        });
      } else {
        for (const r of response.results) {
          newResults.push({
            id: `result-${++resultIdCounter}`,
            input: source,
            output: r.value,
            type: r.type_name,
            isAssignment: r.is_assignment,
            variableName: r.variable_name,
            isError: false,
            timestamp: new Date(),
            imageData: r.image_data ?? undefined,
          });
        }
      }

      set(state => ({
        results: [...state.results, ...newResults],
        variables: response.variables,
        isExecuting: false,
      }));
    } catch (e) {
      set({
        error: e instanceof Error ? e.message : 'Evaluation failed',
        isExecuting: false,
      });
    }
  },

  clearSession: async () => {
    const { sessionId } = get();
    if (!sessionId) return;

    try {
      const response = await api.clearSession(sessionId);
      set({
        variables: response.variables,
        results: [],
        error: null,
      });
    } catch (e) {
      set({ error: e instanceof Error ? e.message : 'Failed to clear session' });
    }
  },

  clearResults: () => {
    set({ results: [] });
  },
}));
