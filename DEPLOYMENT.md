# DevLink Deployment Guide

## 🚀 Production Deployment

### Backend Deployment (Django)

#### 1. Environment Setup
```bash
# Install production dependencies
pip install gunicorn psycopg2-binary whitenoise

# Create production requirements
pip freeze > requirements-prod.txt
```

#### 2. Environment Variables
Create `.env` file:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### 3. Database Migration
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

#### 4. Gunicorn Configuration
Create `gunicorn.conf.py`:
```python
bind = "0.0.0.0:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
```

#### 5. Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/project/staticfiles/;
    }
}
```

### Frontend Deployment (React)

#### 1. Build Production Bundle
```bash
cd devlink-frontend
npm run build
```

#### 2. Serve with Nginx
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    root /path/to/devlink-frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Docker Deployment

#### Backend Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "devlink_backend.wsgi:application"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: devlink
      POSTGRES_USER: devlink
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://devlink:password@db:5432/devlink
    depends_on:
      - db

  frontend:
    build: ./devlink-frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### Cloud Deployment Options

#### 1. Heroku
```bash
# Backend
heroku create devlink-backend
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main

# Frontend
heroku create devlink-frontend
git subtree push --prefix devlink-frontend heroku main
```

#### 2. AWS EC2
- Launch EC2 instance
- Install Docker and Docker Compose
- Clone repository
- Run `docker-compose up -d`

#### 3. DigitalOcean App Platform
- Connect GitHub repository
- Configure build and run commands
- Set environment variables
- Deploy automatically

### Monitoring and Maintenance

#### 1. Log Management
```bash
# View logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
journalctl -u gunicorn -f
```

#### 2. Database Backups
```bash
# PostgreSQL backup
pg_dump devlink > backup_$(date +%Y%m%d).sql

# Restore
psql devlink < backup_20250111.sql
```

#### 3. SSL Certificate
```bash
# Let's Encrypt
certbot --nginx -d yourdomain.com
```

### Performance Optimization

#### Backend
- Enable database connection pooling
- Use Redis for caching
- Implement CDN for static files
- Add database indexes

#### Frontend
- Enable gzip compression
- Implement lazy loading
- Use CDN for assets
- Optimize images

### Security Checklist

- [ ] Change default secret key
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Database encryption
- [ ] API rate limiting
- [ ] Input validation
- [ ] SQL injection prevention

### Backup Strategy

1. **Database**: Daily automated backups
2. **Files**: Weekly backups
3. **Code**: Git repository with tags
4. **Configuration**: Version controlled

### Troubleshooting

#### Common Issues
1. **502 Bad Gateway**: Check Gunicorn status
2. **Static files not loading**: Run collectstatic
3. **Database connection**: Check credentials
4. **CORS errors**: Configure CORS settings
5. **Email not sending**: Check SMTP configuration

#### Health Checks
```bash
# Backend health
curl http://localhost:8000/

# Frontend health
curl http://localhost:3001/

# Database health
psql -c "SELECT 1"
```

---

**Deployment completed successfully! 🎉**

Your DevLink application is now live and ready for users.
