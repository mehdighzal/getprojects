## Environment setup

Backend `.env` keys (create `./.env`):

```
DJANGO_SECRET_KEY=change-me
DEBUG=true
ALLOWED_HOSTS=127.0.0.1,localhost,192.168.56.1
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
CORS_ALLOWED_ORIGINS=http://localhost:3001,http://127.0.0.1:3001,http://192.168.56.1:3001
```

Frontend `.env.local` keys (create `./devlink-frontend/.env.local`):

```
REACT_APP_API_BASE_URL=http://127.0.0.1:8000
```
# DevLink Backend

Backend skeleton inspired by the structure of `uniworld` (https://github.com/mehdighzal/uniworld), adapted to help developers find local businesses (restaurants, clubs, real estate, travel agencies, medical studios, dentists, physiotherapists, private schools, beauty centers, artisans, etc.), discover their emails/names, and send individual or bulk emails with AI-generated content.

## 🚀 Quick Start

1. **Create virtual environment and install dependencies**
```bash
py -m venv venv
venv\Scripts\python -m pip install -r requirements.txt
```

2. **Run migrations and start server**
```bash
venv\Scripts\python manage.py migrate
venv\Scripts\python manage.py runserver
```

3. **Access the application**
- API Base: `http://127.0.0.1:8000/api/`
- Admin Panel: `http://127.0.0.1:8000/admin/`

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (JWT)
- `GET /api/auth/me/` - Get current user info

### Businesses
- `GET /api/businesses/` - List businesses with filters
- `POST /api/businesses/` - Create new business entry

**Query Parameters:**
- `country` - Filter by country
- `city` - Filter by city  
- `category` - Filter by business category
- `search` - Search in name, city, country, category

**Business Categories:**
- `restaurant` - Restaurant
- `club` - Club
- `real_estate` - Agenzia Immobiliare
- `travel_agency` - Agenzia Viaggi
- `medical` - Studio Medico
- `technical_studio` - Studio Tecnico
- `dentist` - Dentista
- `physiotherapist` - Fisioterapista
- `private_school` - Scuola Privata
- `beauty_center` - Centro Estetico
- `artisan` - Artigiano
- `other` - Altro

### Email Services
- `POST /api/email/send/` - Send individual or bulk emails

**Request Body:**
```json
{
  "subject": "Partnership Opportunity",
  "body": "Dear Business Owner...",
  "recipients": ["business1@example.com", "business2@example.com"]
}
```

### AI Services
- `POST /api/ai/generate-email/` - Generate personalized email content
- `POST /api/ai/generate-bulk-email/` - Generate bulk email template

**Generate Email Request:**
```json
{
  "business_name": "Restaurant Milano",
  "business_category": "restaurant",
  "developer_name": "John Doe",
  "developer_services": "Web development, mobile apps, digital marketing"
}
```

**Generate Bulk Email Request:**
```json
{
  "category": "restaurant",
  "developer_name": "John Doe", 
  "developer_services": "Web development, mobile apps, digital marketing"
}
```

## 🔧 Usage Examples

### 1. Register and Login
```bash
# Register
curl -X POST "http://127.0.0.1:8000/api/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{"username": "developer", "email": "dev@example.com", "password": "password123"}'

# Login
curl -X POST "http://127.0.0.1:8000/api/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"username": "developer", "password": "password123"}'
```

### 2. Search Businesses
```bash
# Search restaurants in Milan, Italy
curl "http://127.0.0.1:8000/api/businesses/?country=Italy&city=Milan&category=restaurant" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Search all businesses in Rome
curl "http://127.0.0.1:8000/api/businesses/?country=Italy&city=Rome" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 3. Generate AI Email Content
```bash
curl -X POST "http://127.0.0.1:8000/api/ai/generate-email/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "business_name": "Pizza Roma",
    "business_category": "restaurant",
    "developer_name": "Mario Rossi",
    "developer_services": "Website development, online ordering system"
  }'
```

### 4. Send Email
```bash
curl -X POST "http://127.0.0.1:8000/api/email/send/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "subject": "Partnership Opportunity - Pizza Roma",
    "body": "Dear Pizza Roma Team...",
    "recipients": ["info@pizzaroma.com"]
  }'
```

## 🗄️ Database Schema

### Core Models

1. **User** - Django's built-in user model
2. **Business** - Business information with contact details
3. **EmailLog** - Track emails sent through the platform

### Business Model Fields
- `name` - Business name
- `email` - Contact email
- `phone` - Phone number
- `website` - Website URL
- `category` - Business category
- `country` - Country
- `city` - City
- `address` - Physical address
- `created_at` - Creation timestamp

## 🔒 Security Features

- **JWT Authentication** - Secure token-based authentication
- **Input Validation** - All user inputs are validated
- **CSRF Protection** - Django's built-in CSRF protection
- **Permission Classes** - API endpoints require authentication

## 🎯 Workflow

1. **Register/Login** - Create account and get JWT token
2. **Search Businesses** - Find businesses by location and category
3. **Generate Content** - Use AI to create personalized email content
4. **Send Emails** - Send individual or bulk emails to businesses
5. **Track Activity** - Monitor sent emails in EmailLog

## 🚀 Future Enhancements

- **Real AI Integration** - Connect to OpenAI, Claude, or similar services
- **Email Templates** - Pre-built templates for different business types
- **Analytics Dashboard** - Track email open rates and responses
- **Business Discovery** - AI-powered business finding from web scraping
- **Subscription Plans** - Premium features with email quotas
- **Mobile App** - React Native or Flutter companion app

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

**Made with ❤️ for developers seeking to connect with local businesses**


