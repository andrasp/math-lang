export interface EvaluateRequest {
  source: string;
  session_id?: string;
  timeout_ms?: number;
}

export interface EvaluateResult {
  value: string;
  type_name: string;
  is_assignment: boolean;
  variable_name: string | null;
  image_data: string | null;  // Base64-encoded PNG for plot types
}

export interface ErrorDetail {
  message: string;
  line: number | null;
  column: number | null;
}

export interface EvaluateResponse {
  session_id: string;
  results: EvaluateResult[];
  elapsed_ms: number;
  variables: Record<string, { value: string; type: string }>;
  error: ErrorDetail | null;
}

export interface SessionResponse {
  session_id: string;
  created_at: number;
  last_accessed: number;
  variables: Record<string, { value: string; type: string }>;
}

export interface Operation {
  identifier: string;
  friendly_name: string;
  description: string;
  category: string;
}

export interface OperationsResponse {
  operations: Operation[];
}

export interface PlotData2D {
  type: 'PlotData2D';
  x_values: number[];
  y_values: number[];
  title?: string;
  x_label?: string;
  y_label?: string;
}

export interface PlotData3D {
  type: 'PlotData3D';
  x_values: number[];
  y_values: number[];
  z_values: number[][];
  title?: string;
  x_label?: string;
  y_label?: string;
  z_label?: string;
}

export interface HistogramData {
  type: 'HistogramData';
  values: number[];
  bins: number;
  title?: string;
}

export interface ScatterData {
  type: 'ScatterData';
  x_values: number[];
  y_values: number[];
  title?: string;
}

export type PlotData = PlotData2D | PlotData3D | HistogramData | ScatterData;

export interface DisplayResult {
  id: string;
  input: string;
  output: string;
  type: string;
  isAssignment: boolean;
  variableName: string | null;
  isError: boolean;
  timestamp: Date;
  plotData?: PlotData;
  imageData?: string;  // Base64-encoded PNG image
}
