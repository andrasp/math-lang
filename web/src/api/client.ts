import type { EvaluateRequest, EvaluateResponse, SessionResponse, OperationsResponse } from '../types';

const API_BASE = '/api';

export async function evaluate(request: EvaluateRequest): Promise<EvaluateResponse> {
  const response = await fetch(`${API_BASE}/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!response.ok) {
    throw new Error(`Evaluation failed: ${response.statusText}`);
  }
  return response.json();
}

export async function createSession(): Promise<SessionResponse> {
  const response = await fetch(`${API_BASE}/sessions`, {
    method: 'POST',
  });
  if (!response.ok) {
    throw new Error(`Failed to create session: ${response.statusText}`);
  }
  return response.json();
}

export async function getSession(sessionId: string): Promise<SessionResponse> {
  const response = await fetch(`${API_BASE}/sessions/${sessionId}`);
  if (!response.ok) {
    throw new Error(`Failed to get session: ${response.statusText}`);
  }
  return response.json();
}

export async function clearSession(sessionId: string): Promise<SessionResponse> {
  const response = await fetch(`${API_BASE}/sessions/${sessionId}/clear`, {
    method: 'POST',
  });
  if (!response.ok) {
    throw new Error(`Failed to clear session: ${response.statusText}`);
  }
  return response.json();
}

export async function getOperations(): Promise<OperationsResponse> {
  const response = await fetch(`${API_BASE}/operations/`);
  if (!response.ok) {
    throw new Error(`Failed to get operations: ${response.statusText}`);
  }
  return response.json();
}
