# Arkhon Integration Platform

A complete production-ready product ingestion and synchronization platform with React frontend and Python FastAPI backend.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Frontend Structure](#frontend-structure)
- [Database Schema](#database-schema)
- [Development Guide](#development-guide)
- [Deployment](#deployment)

## 🎯 Overview

Arkhon Integration Platform is a comprehensive system for managing product feeds from external sources (like BigBuy), processing them through an ETL pipeline, and synchronizing product data with outbound systems. The platform provides a complete admin interface for managing products, categories, manufacturers, and monitoring system operations.

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   React     │─────▶│   FastAPI    │─────▶│  PostgreSQL │
│  Frontend   │      │   Backend    │      │  Database   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ├─────▶ Redis (Cache/Queue)
                            │
                            ├─────▶ Celery Workers
                            │
                            └─────▶ FTP Servers
```

### Components:

1. **Frontend (React + TypeScript)**
   - Modern SPA with React 18
   - TailwindCSS for styling
   - React Query for data fetching
   - Zustand for state management
   - React Router for navigation

2. **Backend (FastAPI + Python)**
   - Async/await throughout
   - JWT authentication
   - SQLAlchemy 2.x ORM
   - Pydantic validation
   - Structured logging

3. **Background Workers (Celery)**
   - FTP feed fetching
   - CSV import processing
   - Outbound synchronization
   - Scheduled tasks

4. **Database (PostgreSQL/MySQL)**
   - EAV model for flexible attributes
   - Full-text search capabilities
   - Optimized indexes

## ✨ Features

### Authentication & Authorization
- JWT-based authentication with refresh tokens
- Role-based access control (admin, staff, viewer)
- Token rotation for security
- Session management

### Dashboard
- Real-time system metrics
- Product statistics
- Feed processing status
- Activity timeline
- Visual charts and graphs

### Feed Management
- Automated FTP feed fetching
- CSV import with progress tracking
- Server-side filtering and pagination
- Feed retry mechanism
- Detailed import logs
- File preview

### Product Management
- Comprehensive product CRUD
- Advanced filtering and search
- Bulk update operations (price/quantity)
- EAV attribute system
- Image gallery
- Category management
- Manufacturer management

### Outbound Synchronization
- Queue-based job processing
- Retry mechanism with exponential backoff
- Detailed job logs
- Status tracking

### Monitoring & Logs
- System-wide logging
- Real-time log tailing
- Filterable log viewer
- Cron job monitoring
- Manual task triggering

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.109+
- **Database**: PostgreSQL/MySQL with async support
- **ORM**: SQLAlchemy 2.x (async)
- **Migrations**: Alembic
- **Queue**: Celery + Redis
- **Authentication**: python-jose (JWT)
- **Validation**: Pydantic
- **Testing**: pytest + testcontainers

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **Forms**: React Hook Form + Zod
- **Routing**: React Router v6
- **Charts**: Recharts
- **Icons**: Lucide React

### DevOps
- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (production)
- **Process Manager**: Uvicorn (ASGI)
- **Monitoring**: Prometheus metrics

## 📁 Project Structure

```
arkhon/
├── backend/
│   ├── alembic/              # Database migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/           # API endpoints
│   │   │   │   ├── auth.py
│   │   │   │   ├── dashboard.py
│   │   │   │   ├── feeds.py
│   │   │   │   ├── products.py
│   │   │   │   ├── outbound.py
│   │   │   │   ├── manufacturers.py
│   │   │   │   ├── categories.py
│   │   │   │   ├── attributes.py
│   │   │   │   ├── logs.py
│   │   │   │   ├── settings.py
│   │   │   │   └── cron.py
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── config.py      # Settings
│   │   │   ├── database.py    # DB connection
│   │   │   └── security.py    # Auth utils
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── feed.py
│   │   │   ├── product.py
│   │   │   ├── eav.py
│   │   │   ├── outbound.py
│   │   │   └── log.py
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/
│   │   │   ├── ftp_service.py
│   │   │   └── import_service.py
│   │   ├── workers/
│   │   │   ├── celery_app.py
│   │   │   └── tasks.py
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/       # Layout components
│   │   │   ├── shared/       # Reusable UI components
│   │   │   ├── auth/         # Auth components
│   │   │   ├── dashboard/    # Dashboard widgets
│   │   │   ├── feeds/        # Feed components
│   │   │   ├── products/     # Product components
│   │   │   └── ...
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── stores/           # Zustand stores
│   │   ├── hooks/            # Custom hooks
│   │   ├── types/            # TypeScript types
│   │   ├── utils/            # Utilities
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🚀 Installation

### Prerequisites
- Docker & Docker Compose (recommended)
- OR:
  - Python 3.11+
  - Node.js 20+
  - PostgreSQL 14+
  - Redis 7+

### Option 1: Docker (Recommended)

1. **Clone the repository**
```bash
git clone <repository-url>
cd arkhon
```

2. **Configure environment**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your settings
```

3. **Start services**
```bash
docker-compose up -d
```

4. **Run migrations**
```bash
docker-compose exec backend alembic upgrade head
```

5. **Create admin user**
```bash
docker-compose exec backend python -c "
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash
import asyncio

async def create_admin():
    async with AsyncSessionLocal() as db:
        admin = User(
            email='admin@arkhon.com',
            username='admin',
            hashed_password=get_password_hash('admin123'),
            full_name='Admin User',
            role='admin',
            is_active=True
        )
        db.add(admin)
        await db.commit()

asyncio.run(create_admin())
"
```

6. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
alembic upgrade head

# Start backend
uvicorn app.main:app --reload

# In another terminal, start Celery worker
celery -A app.workers.celery_app worker --loglevel=info

# In another terminal, start Celery beat
celery -A app.workers.celery_app beat --loglevel=info
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env

# Start development server
npm run dev
```

## 📚 API Documentation

### Authentication

#### POST /api/v1/auth/login
Login with credentials
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

#### POST /api/v1/auth/refresh
Refresh access token
```json
{
  "refresh_token": "eyJ..."
}
```

#### POST /api/v1/auth/logout
Logout user
```json
{
  "refresh_token": "eyJ..."
}
```

#### GET /api/v1/auth/me
Get current user info

### Dashboard

#### GET /api/v1/dashboard/stats
Get dashboard statistics

Response:
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

#### GET /api/v1/dashboard/timeline
Get activity timeline

### Feeds

#### GET /api/v1/feeds
List inbound feeds (paginated)

Query Parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `entity_code`: Filter by entity
- `status`: Filter by status
- `search`: Search text
- `start_date`: Filter by date range
- `end_date`: Filter by date range

#### GET /api/v1/feeds/{id}
Get feed details

#### GET /api/v1/feeds/{id}/logs
Get feed processing logs

#### POST /api/v1/feeds/{id}/retry
Retry failed feed import

### Products

#### GET /api/v1/products
List products (paginated)

Query Parameters:
- `page`, `page_size`: Pagination
- `sku`, `name`: Filter by text
- `category_id`, `manufacturer_id`: Filter by relations
- `min_price`, `max_price`: Price range
- `min_stock`, `max_stock`: Stock range
- `search`: Full-text search

#### GET /api/v1/products/{id}
Get product details

#### PUT /api/v1/products/{id}
Update product

#### POST /api/v1/products/bulk-update
Bulk update products

Request:
```json
{
  "product_ids": [1, 2, 3],
  "target_field": "price",
  "mode": "percent",
  "value": 10,
  "reason": "10% price increase"
}
```

### Outbound Jobs

#### GET /api/v1/outbound
List outbound jobs

#### GET /api/v1/outbound/{id}
Get job details

#### POST /api/v1/outbound/{id}/retry
Retry failed job

### Manufacturers

#### GET /api/v1/manufacturers
List manufacturers

#### POST /api/v1/manufacturers
Create manufacturer

#### GET /api/v1/manufacturers/{id}
Get manufacturer

#### PUT /api/v1/manufacturers/{id}
Update manufacturer

#### DELETE /api/v1/manufacturers/{id}
Delete manufacturer

### Categories

#### GET /api/v1/categories
List categories

#### GET /api/v1/categories/{id}
Get category

#### GET /api/v1/categories/{id}/products
Get products in category

### Attributes

#### GET /api/v1/attributes
List attributes

#### POST /api/v1/attributes
Create attribute

#### GET /api/v1/attributes/{id}
Get attribute

#### PUT /api/v1/attributes/{id}
Update attribute

#### DELETE /api/v1/attributes/{id}
Delete attribute

### Logs

#### GET /api/v1/logs
List system logs

#### GET /api/v1/logs/tail
Tail logs (real-time)

### Settings

#### GET /api/v1/settings
Get settings

#### POST /api/v1/settings
Update settings

### Cron

#### GET /api/v1/cron/status
Get cron status

#### POST /api/v1/cron/run/{task_name}
Trigger task manually

Available tasks:
- `fetch_feeds`
- `import_feeds`
- `sync_outbound`

## 🎨 Frontend Structure

### Component Hierarchy

```
App
├── SidebarLayout
│   ├── VerticalSideNav
│   ├── TopBar
│   └── PageContainer
│       └── [Page Components]
```

### Key Components

#### Layout Components
- `SidebarLayout`: Main layout with sidebar
- `VerticalSideNav`: Navigation sidebar
- `TopBar`: Top navigation bar
- `PageContainer`: Page wrapper

#### Shared Components
- `DataTable`: Reusable table with pagination
- `FilterBar`: Filter controls
- `Pagination`: Pagination component
- `Modal`: Modal dialog
- `ConfirmDialog`: Confirmation dialog
- `LoadingSpinner`: Loading indicator
- `EmptyState`: Empty state message
- `ErrorBanner`: Error display

#### Input Components
- `TextInput`, `NumberInput`, `Textarea`
- `Select`, `MultiSelect`
- `DateRangePicker`
- `SearchInput`
- `Toggle`

### State Management

#### Auth Store (Zustand)
```typescript
const { user, isAuthenticated, login, logout } = useAuthStore();
```

#### React Query for Data Fetching
```typescript
const { data, isLoading, error } = useQuery({
  queryKey: ['products', filters],
  queryFn: () => productsApi.list(filters),
});
```

## 🗄️ Database Schema

### Core Tables

**users**
- Authentication and user management
- Role-based access control

**inbound_feeds**
- Track imported feed files
- Processing status and statistics

**outbound_jobs**
- Outbound synchronization jobs
- Retry mechanism

**products**
- Core product data
- Unique constraint on (sku, entity_code)

**manufacturers**
- Manufacturer information

**categories**
- Hierarchical category structure
- Path-based navigation

**attributes** (EAV)
- Flexible attribute definitions
- Support multiple data types

**attribute_values** (EAV)
- Product attribute values
- Type-specific columns

**system_logs**
- Comprehensive system logging

## 💻 Development Guide

### Backend Development

#### Adding a New API Endpoint

1. Create schema in `backend/app/schemas/`
2. Add endpoint in `backend/app/api/v1/`
3. Register in router

Example:
```python
# schemas/widget.py
class WidgetResponse(BaseModel):
    id: int
    name: str

# api/v1/widgets.py
@router.get("", response_model=PaginatedResponse[WidgetResponse])
async def list_widgets(db: AsyncSession = Depends(get_db)):
    # Implementation
    pass
```

#### Running Tests

```bash
cd backend
pytest
pytest --cov=app tests/
```

#### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Frontend Development

#### Adding a New Page

1. Create page component in `src/pages/`
2. Add route in `App.tsx`
3. Add navigation link in `SidebarLayout`

#### Adding API Integration

```typescript
// src/services/index.ts
export const widgetsApi = {
  list: (params: FilterParams) =>
    apiClient.get<PaginatedResponse<Widget>>('/widgets', params),
};

// In component
const { data } = useQuery({
  queryKey: ['widgets'],
  queryFn: () => widgetsApi.list({}),
});
```

#### Building for Production

```bash
cd frontend
npm run build
```

## 🚢 Deployment

### Production Deployment

1. **Build images**
```bash
docker-compose -f docker-compose.prod.yml build
```

2. **Configure secrets**
- Use environment variables or secrets management
- Update `SECRET_KEY`
- Configure database credentials
- Set FTP credentials

3. **Run migrations**
```bash
docker-compose -f docker-compose.prod.yml run backend alembic upgrade head
```

4. **Start services**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables

See `backend/.env.example` for all configuration options.

### Scaling

- Scale Celery workers:
```bash
docker-compose up -d --scale celery-worker=3
```

- Use load balancer for backend API
- Implement CDN for frontend static assets
- Use managed database service

## 📝 License

MIT License - see LICENSE file

## 👥 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ using React, FastAPI, and modern web technologies**
