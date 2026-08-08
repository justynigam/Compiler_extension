export interface ExecutionRequest {
  language: string;
  code: string;
  input: string;
}

export interface ExecutionResponse {
  status: string;
  output: string;
  error: string;
  executionTime: number;
  memory: number;
  exitCode: number;
}

export interface SavedProgram {
  id: number;
  language: string;
  title: string;
  code: string;
  createdAt: string;
  updatedAt: string;
}