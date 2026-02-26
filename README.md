# Django Role-Based Authentication System

A secure Role-Based Authentication API built using Django REST Framework.

This project implements a complete authentication workflow with:

- Role-Based Access Control (RBAC)
- Email Verification (SendGrid SMTP)
- Admin Approval System
- JWT Authentication
- Account Activation / Deactivation
- Admin Password Reset
- Login Rate Limiting
- User Activity Logging
- Strong Password Validation
- Proper Error Handling

---

## 🚀 Features

### 👥 User Roles
- Admin
- Manager
- Customer

### 🔐 Authentication Flow

1. User registers
2. Email verification required
3. Admin approval required
4. User logs in using JWT
5. Role-based access control enforced

---

## 🛠 Tech Stack

- Python 3.x
- Django
- Django REST Framework
- SimpleJWT
- SendGrid SMTP
- SQLite / PostgreSQL

---

## 📦 Installation Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/django-role-based-auth-system.git
cd django-role-based-auth-system
2️⃣ Create Virtual Environment
python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3️⃣ Install Required Packages

You can install manually:

pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install python-dotenv

OR simply run:

pip install -r requirements.txt
4️⃣ Generate requirements.txt (Optional)

If needed:

pip freeze > requirements.txt
5️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate
6️⃣ Create Superuser (Admin)
python manage.py createsuperuser
7️⃣ Run Development Server
python manage.py runserver

Server runs at:

http://127.0.0.1:8000/
📌 API Endpoints
🔹 Authentication
Method	Endpoint	Description
POST	/api/register/	Register new user
GET	/api/verify-email/<uid>/<token>/	Verify email
POST	/api/login/	Login user
POST	/api/auth/jwt/refresh/	Refresh token
🔹 Admin Endpoints (Admin Only)
Method	Endpoint	Description
GET	/api/admin/pending-users/	View pending users
POST	/api/admin/approve/<id>/	Approve user
POST	/api/admin/reject/<id>/	Reject user
POST	/api/admin/toggle-status/<id>/	Activate/Deactivate user
POST	/api/admin/reset-password/<id>/	Reset user password
GET	/api/admin/user-logs/<id>/	View user activity logs
🔒 Security Features

Email verification required before login

Admin approval required

JWT-based authentication

Role-based permission enforcement

Strong password validation

Account activation/deactivation

Login rate limiting

Proper API error responses

📧 Email Configuration (SendGrid)

Add the following in settings.py:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'YOUR_SENDGRID_API_KEY'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'

⚠️ Never commit your API key. Use .env file in production.

🧪 Testing with Postman

Register user

Verify email

Admin approves user

Login

Use Bearer Token for protected routes

📂 Project Structure
project_root/
│
├── accounts/
├── role_auth_system/
├── manage.py
├── requirements.txt
└── README.md
🔮 Future Improvements

Docker support

Swagger API documentation

Redis-based rate limiting

CI/CD pipeline

Unit testing

Production deployment setup
