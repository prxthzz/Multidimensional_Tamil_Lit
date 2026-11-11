# Deployment Guide & Docker Configuration

## 1. Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

## 2. Docker Compose Deployment

```bash
# Build and run containers
docker-compose up --build -d

# Verify container status
docker-compose ps
```

## 3. Environment Variables (`.env`)
```env
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite:///data/production_tamil_knowledge.db
LLM_PROVIDER=local
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```
