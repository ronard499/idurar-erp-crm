# IDURAR ERP CRM - Django Backend

This is the Django backend for IDURAR ERP CRM, refactored from the original Express.js implementation.

## Features

- RESTful API with Django REST Framework
- JWT Authentication with Simple JWT
- SQLite Database (can be easily switched to other databases)
- Comprehensive models for Clients, Invoices, Quotes, Payments, etc.

## Requirements

- Python 3.8+
- Django 5.2+
- Django REST Framework 3.16+

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```
   python manage.py migrate
   ```
4. Setup initial data:
   ```
   python manage.py setup
   ```
5. Run the server:
   ```
   python run.py
   ```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=sqlite:///db.sqlite3
PORT=8888
```

## API Endpoints

### Authentication

- `POST /api/login` - Login
- `POST /api/logout` - Logout
- `POST /api/forgetpassword` - Request password reset
- `POST /api/resetpassword` - Reset password

### Clients

- `POST /api/client/create` - Create client
- `GET /api/client/read/:id` - Get client by ID
- `PATCH /api/client/update/:id` - Update client
- `DELETE /api/client/delete/:id` - Delete client
- `GET /api/client/list` - Get paginated list of clients
- `GET /api/client/listAll` - Get all clients
- `GET /api/client/filter` - Filter clients
- `GET /api/client/search` - Search clients
- `GET /api/client/summary` - Get client summary

### Invoices, Quotes, Payments

Similar endpoints are available for invoices, quotes, and payments.

## Default Admin User

- Email: admin@demo.com
- Password: admin123