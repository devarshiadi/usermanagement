# UserManagement

A modern, mobile-first Student & Admin Management Portal built with FastAPI, SQLAlchemy, Jinja2, and Bootstrap 5. Designed for beautiful aesthetics, robust user/admin flows, and seamless experience on both desktop and mobile. Endorsed by **curseofwitcher**. All rights reserved. Licensed under the MIT License.

[![GitHub](https://img.shields.io/badge/GitHub-usermanagement-blue?logo=github)](https://github.com/devarshiadi/usermanagement)

---

## 🚀 Features

- **User Registration & Login** (with hashed passwords)
- **User Profile & Educational Details** (CRUD)
- **Admin Dashboard**: View, edit, delete users
- **Modern UI/UX**: Mobile-first, Bootstrap 5, custom CSS, gradient buttons, animated cards
- **Session-based Authentication** (secure cookies)
- **SQLite Database** (easy deployment)
- **Hugging Face Spaces Ready** (Docker support, runs on port 7860)

---

## 🛠️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend**: [Jinja2](https://jinja.palletsprojects.com/), [Bootstrap 5](https://getbootstrap.com/)
- **ORM/DB**: [SQLAlchemy](https://www.sqlalchemy.org/) + SQLite
- **Auth**: [passlib](https://passlib.readthedocs.io/) (bcrypt), [itsdangerous](https://itsdangerous.palletsprojects.com/)
- **Forms**: [python-multipart](https://andrew-d.github.io/python-multipart/)
- **Server**: [uvicorn](https://www.uvicorn.org/)
- **Containerization**: Docker

---

## 📦 Python Requirements

All requirements are listed in `requirements.txt`:

| Package            | Purpose                                                  |
|--------------------|----------------------------------------------------------|
| fastapi            | Main web framework                                       |
| uvicorn            | ASGI server to run FastAPI                               |
| jinja2             | HTML templating engine                                   |
| sqlalchemy         | ORM for SQLite database                                  |
| passlib[bcrypt]    | Secure password hashing                                  |
| python-multipart   | Form parsing for file uploads & form data                |
| itsdangerous       | Secure session management                                |

---

## 🖥️ Local Installation & Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/devarshiadi/usermanagement.git
   cd usermanagement
   ```
2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the app locally**
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 7860
   ```
5. **Access the app**
   - Open [http://127.0.0.1:7860](http://127.0.0.1:7860) in your browser.

---

## 🐳 Deploy on Hugging Face Spaces (or Docker)

1. **Build and run with Docker:**
   ```bash
   docker build -t usermanagement .
   docker run -p 7860:7860 usermanagement
   ```
2. **On Hugging Face Spaces:**
   - Push your code (including `Dockerfile` and `requirements.txt`) to your Space.
   - Spaces will automatically build and run the app on port 7860.

---

## 📁 Project Structure

```
usermanagement/
├── main.py              # FastAPI app entrypoint
├── models.py            # SQLAlchemy models
├── database.py          # DB connection & session
├── auth.py              # Authentication helpers
├── requirements.txt     # Python dependencies
├── Dockerfile           # For containerized deploy
├── static/
│   └── custom.css       # Custom CSS for UI/UX
├── templates/
│   ├── base.html        # Base template
│   ├── login.html       # Login page
│   ├── signup.html      # Signup page
│   ├── user_form.html   # User profile form
│   ├── admin_dashboard.html # Admin dashboard
│   ├── admin_edit.html  # Admin edit user
│   └── admin_view.html  # Admin view user
└── ...                  # Other files
```

---

## 📝 License

MIT License

Copyright (c) 2025 curseofwitcher

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

> **Endorsed by curseofwitcher. All rights reserved.**
