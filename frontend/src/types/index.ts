// Core Types for Arkhon Integration Platform

export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string | null;
  role: 'admin' | 'staff' | 'viewer';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface InboundFeed {
  id: number;
  entity_code: string;
  file_name: string;
  file_path: string;
  file_size: number | null;
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'partial';
  total_count: number;
  success_count: number;
  error_count: number;
  pending_count: number;
  started_at: string | null;
  completed_at: string | null;
  error_message: string | null;
  processing_logs: string | null;
  created_at: string;
  updated_at: string;
}

export interface OutboundJob {
  id: number;
  sync_id: string;
  job_type: string;
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'retrying';
  skus: string | null;
  bulk_data: string | null;
  total_count: number;
  success_count: number;
  error_count: number;
  retry_count: number;
  max_retries: number;
  message: string | null;
  processing_logs: string | null;
  started_at: string | null;
  completed_at: string | null;
  next_retry_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: number;
  sku: string;
  entity_code: string;
  name: string;
  description: string | null;
  price: string;
  cost: string | null;
  retail_price: string | null;
  qty: number;
  min_qty: number;
  manufacturer_id: number | null;
  manufacturer: Manufacturer | null;
  images: string | null;
  raw_data: string | null;
  is_active: number;
  categories: Category[];
  attributes: AttributeValue[];
  created_at: string;
  updated_at: string;
}

export interface Manufacturer {
  id: number;
  name: string;
  code: string | null;
  description: string | null;
  website: string | null;
  is_system: number;
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: number;
  name: string;
  code: string | null;
  parent_id: number | null;
  description: string | null;
  level: number;
  path: string | null;
  product_count?: number;
  created_at: string;
  updated_at: string;
}

export interface Attribute {
  id: number;
  code: string;
  label: string;
  attribute_type: 'varchar' | 'text' | 'int' | 'decimal' | 'datetime' | 'boolean';
  input_type: 'text' | 'textarea' | 'select' | 'multiselect' | 'number' | 'date' | 'boolean';
  options: string | null;
  validation_rules: string | null;
  is_system: number;
  is_searchable: number;
  is_filterable: number;
  sort_order: number;
  group_name: string | null;
  usage_count?: number;
  created_at: string;
  updated_at: string;
}

export interface AttributeValue {
  attribute_id: number;
  attribute_code: string;
  attribute_label: string;
  value: any;
}

export interface SystemLog {
  id: number;
  log_type: 'import' | 'export' | 'cron' | 'auth' | 'api' | 'system';
  log_level: 'debug' | 'info' | 'warning' | 'error' | 'critical';
  message: string;
  context: string | null;
  user_id: number | null;
  ip_address: string | null;
  entity_type: string | null;
  entity_id: number | null;
  created_at: string;
}

export interface DashboardStats {
  total_products: number;
  total_outbound_jobs: number;
  pending_inbound_feeds: number;
  failed_inbound_feeds: number;
  queue_status: {
    pending: number;
  };
  recent_activity: {
    products_last_7_days: number;
    feeds_last_7_days: number;
  };
}

export interface BulkUpdateRequest {
  product_ids: number[];
  target_field: 'price' | 'qty';
  mode: 'percent' | 'fixed';
  value: number;
  reason?: string;
}

export interface BulkUpdatePreview {
  product_id: number;
  sku: string;
  name: string;
  old_value: string;
  new_value: string;
}

export interface FilterParams {
  page?: number;
  page_size?: number;
  search?: string;
  [key: string]: any;
}
