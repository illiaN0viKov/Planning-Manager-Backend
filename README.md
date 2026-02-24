# ⚙️ Planning Manager - Backend (Django)

This is the **Django** REST API for the Planning Manager. It handles the database, business logic, and provides endpoints for the Next.js frontend.

---

## 🏗️ Prerequisites

Ensure you have the following installed:
* **Python 3.10+**
* **pip** (Python package manager)
* **Virtualenv** (Recommended)

---

## 🚀 Getting Started

### 1. Clone and Setup Environment
```bash
git clone [https://github.com/illiaN0viKov/Planning-Manager.git](https://github.com/illiaN0viKov/Planning-Manager.git)
cd Planning-Manager
python -m venv venv
source venv/scripts/activate
pip install requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
