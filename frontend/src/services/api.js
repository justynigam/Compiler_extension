import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

export async function fetchDatasets() {
  const { data } = await api.get('/datasets/');
  return data;
}

export async function uploadDataset(formData) {
  const { data } = await api.post('/datasets/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
}

export async function fetchModels() {
  const { data } = await api.get('/models/');
  return data;
}

export async function createModel(body) {
  const { data } = await api.post('/models/', body);
  return data;
}

export async function getModel(id) {
  const { data } = await api.get(`/models/${id}`);
  return data;
}

export async function trainModel(id, body) {
  const { data } = await api.post(`/models/${id}/train`, body);
  return data;
}

export async function predictModel(id, body) {
  const { data } = await api.post(`/models/${id}/predict`, body);
  return data;
}

export async function explainModel(id, body) {
  const { data } = await api.post(`/models/${id}/explain`, body);
  return data;
}

export async function graphAnalysis(id) {
  const { data } = await api.get(`/models/${id}/graph`);
  return data;
}