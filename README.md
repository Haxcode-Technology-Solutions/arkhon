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

## 🚀 Installation & Configuration

### Prerequisites

**For Local Development (Docker):**
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git

**For Manual Installation:**
- Python 3.11+
- Node.js 20+
- PostgreSQL 14+ or MySQL 8+
- Redis 7+
- Git

**For Production Server:**
- Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- Docker & Docker Compose
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)

---

## 📦 Local Installation with Docker

This is the **recommended** method for local development and testing.

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/arkhon.git
cd arkhon
```

### Step 2: Configure Environment Variables

```bash
# Copy the example environment file
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your preferred text editor:

```bash
nano backend/.env
# or
vim backend/.env
# or
code backend/.env
```

**Required Configuration:**

```env
# Application
APP_NAME=Arkhon Integration Platform
DEBUG=True  # Set to False in production

# Security (CHANGE THIS!)
SECRET_KEY=your-super-secret-key-change-this-in-production-use-at-least-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database (Docker defaults)
DATABASE_URL=postgresql+asyncpg://arkhon:arkhon_password@postgres:5432/arkhon

# Redis (Docker defaults)
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# CORS (Allow frontend access)
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# File Storage
STORAGE_TYPE=local
LOCAL_STORAGE_PATH=./storage

# FTP Settings (Configure for your data source)
BIGBUY_FTP_HOST=ftp.bigbuy.eu
BIGBUY_FTP_PORT=21
BIGBUY_FTP_USER=your-ftp-username
BIGBUY_FTP_PASSWORD=your-ftp-password
BIGBUY_FTP_PATH=/products

# Import Settings
CSV_CHUNK_SIZE=1000
MAX_IMPORT_ERRORS=100

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Start All Services

```bash
# Start all containers in detached mode
docker-compose up -d

# Verify all services are running
docker-compose ps
```

You should see 6 services running:
- `arkhon-postgres` (Database)
- `arkhon-redis` (Cache/Queue)
- `arkhon-backend` (FastAPI)
- `arkhon-celery-worker` (Background tasks)
- `arkhon-celery-beat` (Scheduler)
- `arkhon-frontend` (React app)

### Step 4: Initialize Database

```bash
# Run database migrations
docker-compose exec backend alembic upgrade head

# Verify migration success
docker-compose exec backend alembic current
```

### Step 5: Create Admin User

```bash
# Create the admin user
docker-compose exec backend python -c "
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash
import asyncio

async def create_admin():
    async with AsyncSessionLocal() as db:
        # Check if admin already exists
        from sqlalchemy import select
        result = await db.execute(select(User).where(User.email == 'admin@arkhon.com'))
        existing = result.scalar_one_or_none()

        if existing:
            print('Admin user already exists')
            return

        admin = User(
            email='admin@arkhon.com',
            username='admin',
            hashed_password=get_password_hash('admin123'),
            full_name='System Administrator',
            role='admin',
            is_active=True
        )
        db.add(admin)
        await db.commit()
        print('Admin user created successfully!')
        print('Email: admin@arkhon.com')
        print('Password: admin123')
        print('⚠️  IMPORTANT: Change this password after first login!')

asyncio.run(create_admin())
"
```

### Step 6: Access the Application

Open your browser and navigate to:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **OpenAPI Spec:** http://localhost:8000/redoc

**Default Login Credentials:**
- Email: `admin@arkhon.com`
- Password: `admin123`

⚠️ **Change the default password immediately after first login!**

### Step 7: Verify Installation

```bash
# Check backend logs
docker-compose logs -f backend

# Check celery worker logs
docker-compose logs -f celery-worker

# Check frontend logs
docker-compose logs -f frontend

# View all logs
docker-compose logs -f
```

### Common Docker Commands

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ deletes all data)
docker-compose down -v

# Restart a specific service
docker-compose restart backend

# View logs for a specific service
docker-compose logs -f backend

# Execute commands in a container
docker-compose exec backend bash

# Rebuild containers after code changes
docker-compose up -d --build

# View resource usage
docker stats
```

---

## 🖥️ Server Installation & Configuration

Complete guide for deploying to a production server.

### Prerequisites

- Ubuntu 20.04+ server with at least 2GB RAM
- Root or sudo access
- Domain name pointed to your server (optional)
- Open ports: 80 (HTTP), 443 (HTTPS), 22 (SSH)

### Step 1: Prepare the Server

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y git curl wget nano ufw

# Configure firewall
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw --force enable

# Verify firewall status
sudo ufw status
```

### Step 2: Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installations
docker --version
docker-compose --version

# Logout and login again for group changes to take effect
exit
# SSH back into the server
```

### Step 3: Clone and Configure Application

```bash
# Create application directory
sudo mkdir -p /opt/arkhon
sudo chown $USER:$USER /opt/arkhon
cd /opt/arkhon

# Clone repository
git clone https://github.com/your-org/arkhon.git .

# Create production environment file
cp backend/.env.example backend/.env
nano backend/.env
```

**Production Environment Configuration:**

```env
# Application
APP_NAME=Arkhon Integration Platform
APP_VERSION=1.0.0
DEBUG=False  # IMPORTANT: Must be False in production

# Security - GENERATE NEW SECRET KEY!
SECRET_KEY=CHANGE-THIS-TO-A-SECURE-RANDOM-STRING-AT-LEAST-32-CHARACTERS
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database - Use strong passwords!
DATABASE_URL=postgresql+asyncpg://arkhon:STRONG_DB_PASSWORD_HERE@postgres:5432/arkhon

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# CORS - Add your domain
BACKEND_CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]

# File Storage
STORAGE_TYPE=local
LOCAL_STORAGE_PATH=/app/storage

# FTP Configuration
BIGBUY_FTP_HOST=ftp.bigbuy.eu
BIGBUY_FTP_PORT=21
BIGBUY_FTP_USER=your-production-ftp-user
BIGBUY_FTP_PASSWORD=your-production-ftp-password
BIGBUY_FTP_PATH=/products

# Import & Sync Settings
CSV_CHUNK_SIZE=1000
MAX_IMPORT_ERRORS=100
OUTBOUND_RETRY_ATTEMPTS=3
OUTBOUND_RETRY_DELAY=5

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

**Generate secure credentials:**
```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate database password
python3 -c "import secrets; print(secrets.token_urlsafe(24))"
```

### Step 4: Update Docker Compose for Production

Create a production docker-compose override:

```bash
nano docker-compose.prod.yml
```

```yaml
version: '3.8'

services:
  postgres:
    restart: always
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}  # Use strong password from .env
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    restart: always
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  backend:
    restart: always
    environment:
      - DEBUG=False
    build:
      context: ./backend
      dockerfile: Dockerfile
    volumes:
      - storage_data:/app/storage

  celery-worker:
    restart: always
    environment:
      - DEBUG=False

  celery-beat:
    restart: always
    environment:
      - DEBUG=False

  frontend:
    restart: always
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: production
    ports:
      - "80:80"
    environment:
      - VITE_API_URL=https://yourdomain.com/api/v1

volumes:
  postgres_data:
  redis_data:
  storage_data:
```

### Step 5: Configure Nginx (Optional - for custom domain)

If using a custom domain with SSL:

```bash
# Install Nginx
sudo apt install -y nginx certbot python3-certbot-nginx

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/arkhon
```

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS Configuration
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificates (will be added by certbot)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;

        # Increase timeouts for long-running requests
        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
        send_timeout 600;
    }

    # API Documentation
    location /docs {
        proxy_pass http://localhost:8000/docs;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript application/json;
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/arkhon /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Restart Nginx
sudo systemctl restart nginx

# Enable auto-renewal
sudo systemctl enable certbot.timer
```

### Step 6: Build and Start Production Services

```bash
cd /opt/arkhon

# Build images
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Verify all containers are running
docker-compose ps
```

### Step 7: Initialize Production Database

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Create admin user
docker-compose exec backend python -c "
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash
import asyncio

async def create_admin():
    async with AsyncSessionLocal() as db:
        from sqlalchemy import select
        result = await db.execute(select(User).where(User.email == 'admin@arkhon.com'))
        existing = result.scalar_one_or_none()

        if existing:
            print('Admin user already exists')
            return

        admin = User(
            email='admin@arkhon.com',
            username='admin',
            hashed_password=get_password_hash('CHANGE_THIS_PASSWORD'),
            full_name='System Administrator',
            role='admin',
            is_active=True
        )
        db.add(admin)
        await db.commit()
        print('Admin user created!')

asyncio.run(create_admin())
"
```

### Step 8: Configure Automated Backups

```bash
# Create backup script
sudo nano /usr/local/bin/backup-arkhon.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/arkhon"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
docker exec arkhon-postgres pg_dump -U arkhon arkhon | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup storage files
tar -czf $BACKUP_DIR/storage_$DATE.tar.gz /opt/arkhon/storage/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
# Make executable
sudo chmod +x /usr/local/bin/backup-arkhon.sh

# Add to crontab (daily at 2 AM)
sudo crontab -e
# Add this line:
0 2 * * * /usr/local/bin/backup-arkhon.sh >> /var/log/arkhon-backup.log 2>&1
```

### Step 9: Setup Monitoring (Optional)

```bash
# Install monitoring tools
sudo apt install -y htop nethogs

# View system resources
htop

# Monitor Docker containers
docker stats

# View application logs
docker-compose logs -f backend
docker-compose logs -f celery-worker
```

### Step 10: Production Checklist

✅ **Security:**
- [ ] Changed default SECRET_KEY
- [ ] Changed default admin password
- [ ] Set DEBUG=False
- [ ] Configured firewall (UFW)
- [ ] SSL certificate installed
- [ ] Strong database passwords
- [ ] Updated CORS origins

✅ **Services:**
- [ ] All containers running
- [ ] Database migrations applied
- [ ] Admin user created
- [ ] Celery workers operational
- [ ] Celery beat scheduler running

✅ **Monitoring:**
- [ ] Automated backups configured
- [ ] Log rotation setup
- [ ] Health checks working
- [ ] Error notifications configured

✅ **Performance:**
- [ ] Database indexed properly
- [ ] Redis persistence enabled
- [ ] Nginx caching configured
- [ ] Connection pooling enabled

### Maintenance Commands

```bash
# View logs
docker-compose logs -f [service-name]

# Restart services
docker-compose restart

# Update application
cd /opt/arkhon
git pull
docker-compose build
docker-compose up -d

# Backup database manually
docker exec arkhon-postgres pg_dump -U arkhon arkhon > backup.sql

# Restore database
cat backup.sql | docker exec -i arkhon-postgres psql -U arkhon arkhon

# Clean up old images
docker system prune -a

# Monitor resource usage
docker stats
```

### Troubleshooting

**Services won't start:**
```bash
# Check logs
docker-compose logs backend
docker-compose logs postgres

# Verify environment variables
docker-compose config

# Check disk space
df -h
```

**Database connection errors:**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Test database connection
docker-compose exec postgres psql -U arkhon -d arkhon
```

**High memory usage:**
```bash
# Check resource usage
docker stats

# Restart services
docker-compose restart

# Adjust worker count in docker-compose.yml
```

---

## 🔄 Updating the Application

### Local (Docker):
```bash
cd arkhon
git pull
docker-compose down
docker-compose up -d --build
docker-compose exec backend alembic upgrade head
```

### Production Server:
```bash
cd /opt/arkhon

# Backup first!
/usr/local/bin/backup-arkhon.sh

# Pull updates
git pull

# Rebuild and restart
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Run migrations
docker-compose exec backend alembic upgrade head

# Verify
docker-compose ps
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
