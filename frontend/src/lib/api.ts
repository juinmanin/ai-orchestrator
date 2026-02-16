import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API functions
export const authAPI = {
  register: (email: string, password: string) => 
    api.post('/api/auth/register', { email, password }),
  
  login: (email: string, password: string) => 
    api.post('/api/auth/login', { email, password }),
  
  getMe: () => 
    api.get('/api/auth/me'),
  
  updateMe: (data: any) => 
    api.patch('/api/auth/me', data),
};

export const accountsAPI = {
  list: () => 
    api.get('/api/accounts'),
  
  get: (id: number) => 
    api.get(`/api/accounts/${id}`),
  
  create: (data: any) => 
    api.post('/api/accounts', data),
  
  delete: (id: number) => 
    api.delete(`/api/accounts/${id}`),
  
  verify: (id: number) => 
    api.post(`/api/accounts/${id}/verify`),
};

export const quotaAPI = {
  dashboard: () => 
    api.get('/api/quota/dashboard'),
  
  recommendations: () => 
    api.get('/api/quota/recommendations'),
  
  schedule: () => 
    api.get('/api/quota/schedule'),
  
  getAccount: (id: number) => 
    api.get(`/api/quota/${id}`),
};

export const guidesAPI = {
  list: () => 
    api.get('/api/guides'),
  
  get: (platformId: string) => 
    api.get(`/api/guides/${platformId}`),
};

export default api;
