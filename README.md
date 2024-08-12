# Blog-API
simple blog APIs that demonstrates user authentication, CRUD operations, Django-Ninja and Pydantic schemas.

##  **BLOG API**

This project is a Django REST Framework web application.

**Core Technologies:**

* Python
* Django REST Framework

**Prerequisites:**

* Python 3.x ([https://www.python.org/downloads/](https://www.python.org/downloads/))
* pip (usually comes bundled with Python)

**Installation:**

1. Clone this repository:

```
git clone https://github.com/Jayteemighty/Blog-API.git
```
2. Navigate to the project directory:

```
cd 'blog-api'
```
3. Create a virtual environment (recommended):

```
python -m venv venv
source venv/bin/activate  # For Linux/macOS
source venv/Scripts/activate  # For Windows
```
4. Install project dependencies:

```
pip install -r requirements.txt
```

**Development Setup:**

1. Run database migrations:

```
python manage.py migrate
```
2. Create a superuser account (for initial admin access):

```
python manage.py createsuperuser
```
3. Start the development server:

```
python manage.py runserver
```
3. Access swagger documentation on the development server:

```
http://127.0.0.1:8000/docs/
```

**Additional Notes:**

* This project uses a `.env` file for environment variables (database connection etc.). Configure this file locally following the `.env.example` template.