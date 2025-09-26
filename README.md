# 📝 Todo API

A simple **Task Management REST API** built with **Django + DRF**.  
Supports authentication, categories, filters, bulk actions, and CSV export.  

---

## 🚀 Features
- **User Accounts & JWT Authentication** (register, login, profile)
- **Tasks & Categories CRUD**
- **Mark tasks as done** (idempotent)
- **Smart filters** → `?due=today | overdue | week`
- **Bulk actions** → done & delete multiple tasks in one request
- **CSV export** → `GET /api/tasks/export.csv`
- **Browsable API Docs** (Swagger & Redoc)

---

## ⚙️ Tech Stack
- Django + Django REST Framework
- JWT (djangorestframework-simplejwt)
- drf-spectacular (Swagger / Redoc)
- django-filter (search & filtering)

---

## 📡 API Endpoints (highlights)

**Auth**
- `POST /api/accounts/register/` → create user  
- `POST /api/accounts/token/` → get access/refresh tokens  
- `GET /api/accounts/me/` → current user profile  

**Tasks**
- `GET /api/tasks/` → list tasks (supports filters & ordering)  
- `POST /api/tasks/` → create task  
- `GET /api/tasks/{id}/` → retrieve task  
- `PATCH /api/tasks/{id}/done/` → mark task as done  
- `POST /api/tasks/bulk/done/` → mark multiple tasks done  
- `POST /api/tasks/bulk/delete/` → delete multiple tasks  
- `GET /api/tasks/export.csv` → download tasks as CSV  

**Categories**
- `GET /api/categories/` → list categories  
- `POST /api/categories/` → create category  

---

## 🔑 Usage

1. Clone & install requirements:
   ```bash
   git clone https://github.com/amir-pashayi/todo-api.git
   cd todo-api
   pip install -r requirements.txt
   ```

2. Run migrations & create superuser:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. Start development server:
   ```bash
   python manage.py runserver
   ```

---

## 📖 API Docs
- Swagger UI → [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)  
- Redoc → [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)  

---

## ✨ Author
Developed with ❤️ and ☕ by **Amir Pashayi**
