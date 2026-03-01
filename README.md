🗂 Task Management System (Django + DRF + JWT)

This is a full-stack Task Management System built using Django and Django REST Framework.

The project started as a regular Django web app (HTML + Bootstrap UI) and was later extended with a REST API using JWT authentication and rate limiting.

The main goal was to build something practical with proper structure — not just simple CRUD — but with role-based access, soft delete, filtering, pagination, and security basics.

🚀 Features
🔐 Authentication

Custom User Model (Email as username)

JWT Authentication (Access & Refresh tokens)

Login rate limiting (throttling)

Role-based access control

👤 Users

Create, update, delete users

Role system (Admin / Manager / Employee / User)

/api/users/me/ endpoint

Soft delete support

📋 Tasks

Create, update, delete tasks

Soft delete (no hard deletes)

Role-based task visibility

Assigned user can update task status

Pagination (UI + API)

Filtering by status & priority

Custom change_status API action

📊 Dashboard

Task statistics (total / pending / completed)

API endpoint for summary

🛠 Tech Stack

Python 3.12

Django

Django REST Framework

SimpleJWT

Bootstrap

SQLite

⚙️ Setup

Clone the repository:

git clone [https://github.com/your-username/task-management-system.git](https://github.com/ajumishra5/task-management-system.git)
cd task-management-system

Create virtual environment and install dependencies:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Run migrations and start server:

python manage.py migrate
python manage.py runserver
🔑 API Authentication

Get JWT token:

POST /api/token/
{
  "email": "admin@example.com",
  "password": "yourpassword"
}

Use in header:

Authorization: Bearer <access_token>
📡 Main API Endpoints
Authentication

POST /api/token/

POST /api/token/refresh/

Users

GET /api/users/

POST /api/users/

GET /api/users/<id>/

PATCH /api/users/<id>/

DELETE /api/users/<id>/

GET /api/users/me/

Tasks

GET /api/tasks/

POST /api/tasks/

GET /api/tasks/<id>/

PATCH /api/tasks/<id>/

DELETE /api/tasks/<id>/

PATCH /api/tasks/<id>/change_status/

Dashboard

GET /api/dashboard/

📌 Project Focus

Clean architecture

Custom authentication

Role-based access

Soft delete logic

Security basics (JWT + throttling)

Proper Git workflow

This project was built to strengthen backend fundamentals and simulate a real-world task management system.
