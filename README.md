````markdown
# 🥦 Nutrition API

A small FastAPI project for managing users, foods, and meals — built for learning and experimentation.

---

## 🚀 Setup Instructions

### 1️⃣ Create a virtual environment
```bash
python -m venv venv
````

### 2️⃣ Activate it

**Windows (PowerShell):**

```bash
venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies

You can install everything at once from `requirements.txt` (once you generate it):

```bash
pip install -r requirements.txt
```

---

## 📦 Dependencies Installed

| Library           | Purpose                                 |
| ----------------- | --------------------------------------- |
| `fastapi`         | Web framework for building APIs         |
| `uvicorn`         | ASGI server to run the FastAPI app      |
| `sqlalchemy`      | ORM for database models                 |
| `pydantic`        | Data validation and serialization       |

# TODO: add these libraries
pip install python-jose[cryptography] passlib[bcrypt] python-multipart

---

---

## 🧠 Project structure (so far)

```
nutrition_api/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── database.py
│
├── venv/
├── requirements.txt
└── README.md
```

---

## ▶️ Run the API

```bash
uvicorn app.main:app --reload
```

Then open your browser at:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📝 Notes

* Keep `venv/` out of version control (`.gitignore` it).
* Always activate the venv before running or installing anything.
* Keep your `requirements.txt` updated with `pip freeze > requirements.txt`.

---
