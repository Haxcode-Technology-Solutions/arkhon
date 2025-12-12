# Arkhon Integration Platform - Complete API Specification

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Response Formats

### Success Response
```json
{
  "data": { ... },
  "message": "Success"
}
```

### Error Response
```json
{
  "detail": "Error message",
  "error_code": "OPTIONAL_CODE"
}
```

### Paginated Response
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
}
```

## Endpoints

### 1. Authentication

#### 1.1 Login
**POST** `/auth/login`

Request:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Errors:
- 401: Invalid credentials
- 403: User account inactive

#### 1.2 Refresh Token
**POST** `/auth/refresh`

Request:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Response (200): Same as login

Errors:
- 401: Invalid or expired refresh token

#### 1.3 Logout
**POST** `/auth/logout`

Requires: Authentication

Request:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Response (200):
```json
{
  "message": "Successfully logged out"
}
```

#### 1.4 Get Current User
**GET** `/auth/me`

Requires: Authentication

Response (200):
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "role": "staff",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### 1.5 Register User
**POST** `/auth/register`

Request:
```json
{
  "email": "newuser@example.com",
  "username": "newuser",
  "password": "securepassword123",
  "full_name": "New User",
  "role": "viewer"
}
```

Response (200): User object

Errors:
- 400: Email or username already exists

### 2. Dashboard

#### 2.1 Get Dashboard Stats
**GET** `/dashboard/stats`

Requires: Authentication

Response (200):
```json
{
  "total_products": 15420,
  "total_outbound_jobs": 342,
  "pending_inbound_feeds": 2,
  "failed_inbound_feeds": 1,
  "queue_status": {
    "pending": 5
  },
  "recent_activity": {
    "products_last_7_days": 1250,
    "feeds_last_7_days": 7
  }
}
```

#### 2.2 Get Timeline
**GET** `/dashboard/timeline`

Requires: Authentication

Query Parameters:
- `limit` (optional, default: 20): Number of events

Response (200):
```json
{
  "timeline": [
    {
      "type": "inbound_feed",
      "id": 123,
      "entity_code": "bigbuy",
      "file_name": "products_2024-01-15.csv",
      "status": "completed",
      "timestamp": "2024-01-15T10:30:00Z",
      "details": {
        "total_count": 5000,
        "success_count": 4998,
        "error_count": 2
      }
    },
    {
      "type": "outbound_job",
      "id": 456,
      "sync_id": "bulk_update_abc123",
      "status": "completed",
      "timestamp": "2024-01-15T09:15:00Z",
      "details": {
        "total_count": 100,
        "success_count": 100,
        "error_count": 0
      }
    }
  ]
}
```

### 3. Inbound Feeds

#### 3.1 List Feeds
**GET** `/feeds`

Requires: Authentication

Query Parameters:
- `page` (default: 1)
- `page_size` (default: 20, max: 100)
- `entity_code` (optional): Filter by entity
- `status` (optional): pending, processing, completed, failed, partial
- `search` (optional): Search in file_name, entity_code
- `start_date` (optional): ISO datetime
- `end_date` (optional): ISO datetime

Response (200): Paginated list of feeds

#### 3.2 Get Feed Detail
**GET** `/feeds/{id}`

Requires: Authentication

Response (200):
```json
{
  "id": 123,
  "entity_code": "bigbuy",
  "file_name": "products_2024-01-15.csv",
  "file_path": "/storage/feeds/2024-01-15/bigbuy/products.csv",
  "file_size": 52428800,
  "status": "completed",
  "total_count": 5000,
  "success_count": 4998,
  "error_count": 2,
  "pending_count": 0,
  "started_at": "2024-01-15T10:00:00Z",
  "completed_at": "2024-01-15T10:30:00Z",
  "error_message": null,
  "processing_logs": "[{\"level\": \"info\", \"message\": \"Processing started\"}]",
  "created_at": "2024-01-15T09:55:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

Errors:
- 404: Feed not found

#### 3.3 Get Feed Logs
**GET** `/feeds/{id}/logs`

Requires: Authentication

Response (200):
```json
{
  "feed_id": 123,
  "processing_logs": "[...]",
  "error_message": null
}
```

#### 3.4 Retry Feed
**POST** `/feeds/{id}/retry`

Requires: Authentication, Staff role

Response (200):
```json
{
  "message": "Feed import retry initiated",
  "feed_id": 123
}
```

Errors:
- 400: Feed cannot be retried (wrong status)
- 404: Feed not found

### 4. Outbound Jobs

#### 4.1 List Jobs
**GET** `/outbound`

Requires: Authentication

Query Parameters:
- `page`, `page_size`: Pagination
- `status` (optional): Filter by status

Response (200): Paginated list of jobs

#### 4.2 Get Job Detail
**GET** `/outbound/{id}`

Requires: Authentication

Response (200):
```json
{
  "id": 456,
  "sync_id": "bulk_update_abc123",
  "job_type": "bulk_update",
  "status": "completed",
  "skus": "SKU001,SKU002,SKU003",
  "bulk_data": "{\"target_field\": \"price\", ...}",
  "total_count": 100,
  "success_count": 100,
  "error_count": 0,
  "retry_count": 0,
  "max_retries": 3,
  "message": "Bulk update completed successfully",
  "processing_logs": "[...]",
  "started_at": "2024-01-15T09:00:00Z",
  "completed_at": "2024-01-15T09:15:00Z",
  "next_retry_at": null,
  "created_at": "2024-01-15T08:55:00Z",
  "updated_at": "2024-01-15T09:15:00Z"
}
```

#### 4.3 Retry Job
**POST** `/outbound/{id}/retry`

Requires: Authentication, Staff role

Response (200):
```json
{
  "message": "Outbound job retry initiated",
  "job_id": 456
}
```

Errors:
- 400: Maximum retries reached or job cannot be retried

### 5. Products

#### 5.1 List Products
**GET** `/products`

Requires: Authentication

Query Parameters:
- `page`, `page_size`: Pagination
- `sku`: Filter by SKU (contains)
- `name`: Filter by name (contains)
- `category_id`: Filter by category
- `manufacturer_id`: Filter by manufacturer
- `entity_code`: Filter by entity
- `min_price`, `max_price`: Price range
- `min_stock`, `max_stock`: Stock range
- `search`: Full-text search

Response (200):
```json
{
  "items": [
    {
      "id": 1,
      "sku": "SKU001",
      "name": "Product Name",
      "price": "99.99",
      "qty": 100,
      "manufacturer": {
        "id": 1,
        "name": "Brand Name",
        "code": "BRAND"
      },
      "primary_category": {
        "id": 5,
        "name": "Electronics",
        "code": "electronics"
      },
      "entity_code": "bigbuy",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ],
  "total": 15420,
  "page": 1,
  "page_size": 20,
  "total_pages": 771
}
```

#### 5.2 Get Product Detail
**GET** `/products/{id}`

Requires: Authentication

Response (200):
```json
{
  "id": 1,
  "sku": "SKU001",
  "entity_code": "bigbuy",
  "name": "Product Name",
  "description": "Product description",
  "price": "99.99",
  "cost": "50.00",
  "retail_price": "149.99",
  "qty": 100,
  "min_qty": 10,
  "manufacturer_id": 1,
  "manufacturer": {
    "id": 1,
    "name": "Brand Name",
    "code": "BRAND"
  },
  "images": "https://example.com/image1.jpg,https://example.com/image2.jpg",
  "raw_data": "{\"original_field\": \"value\"}",
  "is_active": 1,
  "categories": [
    {
      "id": 5,
      "name": "Electronics",
      "code": "electronics"
    }
  ],
  "attributes": [
    {
      "attribute_id": 10,
      "attribute_code": "color",
      "attribute_label": "Color",
      "value": "Black"
    },
    {
      "attribute_id": 11,
      "attribute_code": "weight",
      "attribute_label": "Weight",
      "value": "500"
    }
  ],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

#### 5.3 Update Product
**PUT** `/products/{id}`

Requires: Authentication, Staff role

Request:
```json
{
  "name": "Updated Product Name",
  "description": "Updated description",
  "price": "109.99",
  "qty": 150,
  "category_ids": [5, 6],
  "attributes": {
    "color": "Blue",
    "weight": "600"
  }
}
```

Response (200): Updated product object

#### 5.4 Bulk Update Products
**POST** `/products/bulk-update`

Requires: Authentication, Staff role

Request:
```json
{
  "product_ids": [1, 2, 3, 4, 5],
  "target_field": "price",
  "mode": "percent",
  "value": 10,
  "reason": "10% price increase for promotion"
}
```

Fields:
- `target_field`: "price" or "qty"
- `mode`: "percent" or "fixed"
- `value`: numeric value (percentage or fixed amount)

Response (200):
```json
{
  "job_id": 456,
  "sync_id": "bulk_update_abc123",
  "total_products": 5,
  "preview": [
    {
      "product_id": 1,
      "sku": "SKU001",
      "name": "Product 1",
      "old_value": "100.00",
      "new_value": "110.00"
    }
  ],
  "message": "Bulk update job created successfully"
}
```

Errors:
- 404: Some products not found

### 6. Manufacturers

#### 6.1 List Manufacturers
**GET** `/manufacturers`

Requires: Authentication

Response (200): Paginated list

#### 6.2 Create Manufacturer
**POST** `/manufacturers`

Requires: Authentication, Staff role

Request:
```json
{
  "name": "New Brand",
  "code": "NEWBRAND",
  "description": "Brand description",
  "website": "https://example.com"
}
```

Response (200): Created manufacturer object

#### 6.3 Update Manufacturer
**PUT** `/manufacturers/{id}`

Requires: Authentication, Staff role

Request: Same as create (all fields optional)

Response (200): Updated manufacturer

Errors:
- 403: Cannot update system manufacturer

#### 6.4 Delete Manufacturer
**DELETE** `/manufacturers/{id}`

Requires: Authentication, Staff role

Response (200):
```json
{
  "message": "Manufacturer deleted successfully"
}
```

Errors:
- 403: Cannot delete system manufacturer

### 7. Categories

#### 7.1 List Categories
**GET** `/categories`

Requires: Authentication

Response (200): Paginated list

#### 7.2 Get Category Detail
**GET** `/categories/{id}`

Requires: Authentication

Response (200):
```json
{
  "id": 5,
  "name": "Electronics",
  "code": "electronics",
  "parent_id": null,
  "description": "Electronic products",
  "level": 0,
  "path": "Electronics",
  "product_count": 500,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

#### 7.3 Get Category Products
**GET** `/categories/{id}/products`

Requires: Authentication

Query Parameters: Same as product list

Response (200): Paginated product list

### 8. Attributes

#### 8.1 List Attributes
**GET** `/attributes`

Requires: Authentication

Response (200): Paginated list

#### 8.2 Create Attribute
**POST** `/attributes`

Requires: Authentication, Staff role

Request:
```json
{
  "code": "warranty_period",
  "label": "Warranty Period",
  "attribute_type": "varchar",
  "input_type": "select",
  "options": "[\"1 year\", \"2 years\", \"3 years\"]",
  "validation_rules": "{\"required\": true}",
  "is_searchable": 1,
  "is_filterable": 1,
  "sort_order": 10,
  "group_name": "Product Details"
}
```

Attribute Types:
- varchar, text, int, decimal, datetime, boolean

Input Types:
- text, textarea, select, multiselect, number, date, boolean

Response (200): Created attribute

#### 8.3 Get Attribute Detail
**GET** `/attributes/{id}`

Requires: Authentication

Response (200):
```json
{
  "id": 10,
  "code": "color",
  "label": "Color",
  "attribute_type": "varchar",
  "input_type": "select",
  "options": "[\"Black\", \"White\", \"Blue\"]",
  "validation_rules": null,
  "is_system": 1,
  "is_searchable": 1,
  "is_filterable": 1,
  "sort_order": 5,
  "group_name": "Appearance",
  "usage_count": 5420,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

#### 8.4 Update Attribute
**PUT** `/attributes/{id}`

Requires: Authentication, Staff role

Request: Partial update (all fields optional)

Errors:
- 403: Cannot update system attribute

#### 8.5 Delete Attribute
**DELETE** `/attributes/{id}`

Requires: Authentication, Staff role

Errors:
- 403: Cannot delete system attribute

### 9. System Logs

#### 9.1 List Logs
**GET** `/logs`

Requires: Authentication

Query Parameters:
- `page`, `page_size`
- `log_type`: import, export, cron, auth, api, system
- `log_level`: debug, info, warning, error, critical
- `keyword`: Search in message and context
- `start_date`, `end_date`: Date range

Response (200): Paginated log list

#### 9.2 Tail Logs
**GET** `/logs/tail`

Requires: Authentication

Query Parameters:
- `limit` (default: 100, max: 500)
- `log_type` (optional)

Response (200):
```json
{
  "logs": [
    {
      "id": 12345,
      "log_type": "import",
      "log_level": "info",
      "message": "Import completed successfully",
      "context": "{\"feed_id\": 123}",
      "user_id": 1,
      "ip_address": "192.168.1.1",
      "entity_type": "feed",
      "entity_id": 123,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### 10. Settings

#### 10.1 Get Settings
**GET** `/settings`

Requires: Authentication, Admin role

Response (200):
```json
{
  "entity_settings": {
    "bigbuy": {
      "enabled": true,
      "entity_code": "bigbuy",
      "name": "BigBuy"
    }
  },
  "ftp_settings": {
    "bigbuy": {
      "host": "ftp.bigbuy.eu",
      "port": 21,
      "username": "****",
      "path": "/products"
    }
  },
  "storage_settings": {
    "type": "local",
    "path": "./storage"
  },
  "sync_settings": {
    "retry_attempts": 3,
    "retry_delay": 5,
    "batch_size": 1000
  }
}
```

#### 10.2 Update Settings
**POST** `/settings`

Requires: Authentication, Admin role

Request: Same structure as get response

Response (200): Updated settings

### 11. Cron & Task Management

#### 11.1 Get Cron Status
**GET** `/cron/status`

Requires: Authentication

Response (200):
```json
{
  "tasks": [
    {
      "name": "fetch_feeds",
      "description": "Fetch product feeds from FTP",
      "schedule": "0 2 * * *",
      "last_run": "2024-01-15T02:00:00Z",
      "next_run": "2024-01-16T02:00:00Z",
      "status": "active",
      "last_status": "success"
    }
  ],
  "worker_status": {
    "active": true,
    "workers": 3,
    "pending_tasks": 5
  }
}
```

#### 11.2 Trigger Task Manually
**POST** `/cron/run/{task_name}`

Requires: Authentication, Staff role

Available tasks:
- `fetch_feeds`: Fetch feeds from FTP
- `import_feeds`: Import latest pending feed
- `sync_outbound`: Sync outbound products

Response (200):
```json
{
  "message": "Task 'fetch_feeds' triggered successfully",
  "task_name": "fetch_feeds",
  "triggered_by": "admin",
  "triggered_at": "2024-01-15T10:00:00Z"
}
```

Errors:
- 400: Invalid task name

## Error Codes

| Status | Description |
|--------|-------------|
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 422 | Validation Error - Invalid data format |
| 500 | Internal Server Error |

## Rate Limiting

Currently not implemented, but recommended for production:
- 100 requests per minute per user
- 1000 requests per hour per user

## Webhooks (Future Enhancement)

Webhook endpoints for event notifications:
- Feed import completed
- Outbound sync completed
- System errors

## WebSocket (Future Enhancement)

Real-time updates for:
- Log tailing
- Progress tracking
- System notifications
