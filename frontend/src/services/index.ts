import apiClient from './api';
import type {
  User,
  PaginatedResponse,
  InboundFeed,
  OutboundJob,
  Product,
  Manufacturer,
  Category,
  Attribute,
  SystemLog,
  DashboardStats,
  BulkUpdateRequest,
  FilterParams,
} from '@/types';

// Dashboard API
export const dashboardApi = {
  getStats: () => apiClient.get<DashboardStats>('/dashboard/stats'),
  getTimeline: (limit = 20) => apiClient.get('/dashboard/timeline', { limit }),
};

// Feeds API
export const feedsApi = {
  list: (params: FilterParams) =>
    apiClient.get<PaginatedResponse<InboundFeed>>('/feeds', params),
  get: (id: number) => apiClient.get<InboundFeed>(`/feeds/${id}`),
  getLogs: (id: number) => apiClient.get(`/feeds/${id}/logs`),
  retry: (id: number) => apiClient.post(`/feeds/${id}/retry`),
};

// Outbound API
export const outboundApi = {
  list: (params: FilterParams) =>
    apiClient.get<PaginatedResponse<OutboundJob>>('/outbound', params),
  get: (id: number) => apiClient.get<OutboundJob>(`/outbound/${id}`),
  retry: (id: number) => apiClient.post(`/outbound/${id}/retry`),
};

// Products API
export const productsApi = {
  list: (params: FilterParams) =>
    apiClient.get<PaginatedResponse<Product>>('/products', params),
  get: (id: number) => apiClient.get<Product>(`/products/${id}`),
  update: (id: number, data: Partial<Product>) =>
    apiClient.put<Product>(`/products/${id}`, data),
  bulkUpdate: (data: BulkUpdateRequest) =>
    apiClient.post('/products/bulk-update', data),
};

// Manufacturers API
export const manufacturersApi = {
  list: (params: FilterParams) =>
    apiClient.get<PaginatedResponse<Manufacturer>>('/manufacturers', params),
  get: (id: number) => apiClient.get<Manufacturer>(`/manufacturers/${id}`),
  create: (data: Partial<Manufacturer>) =>
    apiClient.post<Manufacturer>('/manufacturers', data),
  update: (id: number, data: Partial<Manufacturer>) =>
    apiClient.put<Manufacturer>(`/manufacturers/${id}`, data),
  delete: (id: number) => apiClient.delete(`/manufacturers/${id}`),
};

// Categories API
export const categoriesApi = {
  list: (params: FilterParams) =>
    apiClient.get<PaginatedResponse<Category>>('/categories', params),
  get: (id: number) => apiClient.get<Category>(`/categories/${id}`),
  getProducts: (id: number, params: FilterParams) =>
    apiClient.get<PaginatedResponse<Product>>(`/categories/${id}/products`, params),
};

// Attributes API
export const attributesApi = {
  list: (params: FilterParams) =>
    apiClient.get<PaginatedResponse<Attribute>>('/attributes', params),
  get: (id: number) => apiClient.get<Attribute>(`/attributes/${id}`),
  create: (data: Partial<Attribute>) =>
    apiClient.post<Attribute>('/attributes', data),
  update: (id: number, data: Partial<Attribute>) =>
    apiClient.put<Attribute>(`/attributes/${id}`, data),
  delete: (id: number) => apiClient.delete(`/attributes/${id}`),
};

// Logs API
export const logsApi = {
  list: (params: FilterParams) =>
    apiClient.get<PaginatedResponse<SystemLog>>('/logs', params),
  tail: (params?: any) => apiClient.get('/logs/tail', params),
};

// Settings API
export const settingsApi = {
  get: () => apiClient.get('/settings'),
  update: (data: any) => apiClient.post('/settings', data),
};

// Cron API
export const cronApi = {
  getStatus: () => apiClient.get('/cron/status'),
  runTask: (taskName: string) => apiClient.post(`/cron/run/${taskName}`),
};
