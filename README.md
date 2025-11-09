````markdown
# 🥦 Nutrition API

A modular **FastAPI** backend for managing users, foods, and meals 
— built for learning, experimentation, and good backend practices.


---

## ⚙️ Overview

This project explores how to design a clean and extensible API using **FastAPI**, **SQLAlchemy**, **Pydantic**, and **JWT-based authentication**.  
It includes examples of:

- ✅ User management (registration, authentication)
- 🍎 CRUD operations for foods and meals
- 🔒 Security layers (JWT, hashing, rate-limiting)
- ⚡ Performance features (caching, async DB sessions)
- 🧩 Hexagonal-inspired modular architecture for scalability (in )

---

## 🚀 Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/nutrition-api.git
cd nutrition-api
```

### 2️⃣ Create a virtual environment
```bash
python -m venv venv
```

### 3️⃣ Activate it

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

4️⃣ (Optional) Run Redis for caching and rate-limiting

```bash
docker run -d -p 6379:6379 --name redis-cont redis
```

## ▶️ Run the API

```bash
uvicorn app.main:app --reload

```

Then open your browser at:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


---

## 📦 Dependencies Installed

| Library                     | Purpose                                                |
| --------------------------- | -------------------------------------------------------|
| `fastapi`                   | Web framework for APIs                                 |
| `uvicorn`                   | ASGI server                                            |
| `sqlalchemy`                | ORM for data models                                    |
| `pydantic`                  | Data validation and serialization                      |
| `slowapi`                   | Rate limiting (anti-abuse, DoS prevention)             |
| `fastapi-cache2`            | Caching layer for performance                          |
| `python-jose[cryptography]` | JWT creation and validation                            |
| `passlib[argon2]`           | Recommended, modern and memory hard password hashing   |
| `python-multipart`          | Form and file handling                                 |
| `pydantic-settings`         | Loading config class form .env                         |
| `redis`                     | Key-based in memory cache layer (high performance      |
|                             | persistence, several DS, expiration, logs, async,      |
|                             | support, etc. )                                        |

---

## 🔐 Environment Configuration

This project uses **pydantic-settings** (built on top of `python-dotenv`)  
to manage environment variables safely and consistently.

All sensitive or configurable values (e.g. database URL, secret key, algorithm, etc.)  
are stored in a local `.env` file, which is **not committed** to version control.

To get started:

```bash
cp .env.example .env
```

Then edit .env with your real credentials.

---

## 🧠 Project structure (so far)

```
nutrition_api/
│
├── app/
│   ├── main.py           # FastAPI entrypoint
│   ├── database.py       # SQLAlchemy engine and session
│   ├── models.py         # ORM models
│   ├── schemas.py        # Pydantic DTOs
│   ├── routers/          # Route definitions (users, foods, meals, etc.)
│   ├── services/         # Business logic and reusable modules
│   ├── core/             # Auth, config, and utilities
│   └── tests/            # Pytest unit/integration tests
│
├── requirements.txt
├── .env.example          # Example environment configuration
├── .gitignore
└── README.md
```

---

## 🧪 Development Notes

* Use `pip freeze > requirements.txt` to update dependencies.
* Keep `venv/` out of version control.
* For testing:

  ```bash
  pytest -v
  ```
* To format your code:

  ```bash
  black .
  ```

---

## 🧭 Roadmap

* [X] Add JWT authentication routes (`/auth/login`, `/auth/register`)
* [X] .env config with pydantic
* [X] SQLite DB for local development
* [X] RESTful foods CRUD
* [X] RESTful foods schemas
* [X] RESTful meals CRUD
* [X] RESTful meals schemas
* [X] RESTful users CRUD
* [X] RESTful users schemas
* [ ] RESTful roles CRUD
* [ ] RESTful roles schemas
* [ ] RESTful permissions CRUD
* [ ] RESTful permissions schemas
* [X] Implement rate-limiting
* [X] Role based access control (RBAC).
* [ ] Add `fastapi-cache2` for static food data
* [ ] Dockerize the app with separate dev/prod configurations
* [ ] Add Alembic migrations
* [ ] Create CI pipeline for linting & testing
* [ ] Refactor to Hexagonal
* [ ] Deploy V0

---

## 💡 Inspiration

This project is part of my backend learning journey, combining modern FastAPI practices with clean architecture principles.
Think of it as a *playground for backend craftsmanship* 🧠

---

## 🧑‍💻 Author

**Darian Delgado Crespo**
Backend Developer • Python & Symfony
🌐 [LinkedIn](https://www.linkedin.com/in/darian-delgado-crespo-153b7937a/)

---