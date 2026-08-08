import axios from 'axios';
import type { ExecutionRequest, ExecutionResponse, SavedProgram } from '../types';

const api = axios.create({
  baseURL: 'http://localhost:8080/api/compiler',
  timeout: 30000,
});

export async function runCode(request: ExecutionRequest): Promise<ExecutionResponse> {
  const response = await api.post<ExecutionResponse>('/run', request);
  return response.data;
}

export async function saveProgram(request: {
  language: string;
  title: string;
  code: string;
}): Promise<SavedProgram> {
  const response = await api.post<SavedProgram>('/save', request);
  return response.data;
}

export async function getProgram(id: number): Promise<SavedProgram> {
  const response = await api.get<SavedProgram>(`/${id}`);
  return response.data;
}

export async function getAllPrograms(): Promise<SavedProgram[]> {
  const response = await api.get<SavedProgram[]>('/all');
  return response.data;
}

export async function deleteProgram(id: number): Promise<void> {
  await api.delete(`/${id}`);
}