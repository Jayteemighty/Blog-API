# Blog-API

Simple blog APIs that demonstrate Django-Ninja, Pydantic schemas, user authentication and CRUD operations.

## **BLOG API**

This project is a Django REST Framework web application.

**Core Technologies:**

* Python
* Django REST Framework
* [PostgreSQL](https://www.postgresql.org/download/)

**Prerequisites:**

* Python 3.x ([https://www.python.org/downloads/](https://www.python.org/downloads/))
* pip (usually comes bundled with Python)
* [PostgreSQL](https://www.postgresql.org/download/)

**Installation:**

1. Clone this repository:

    ```bash
    git clone https://github.com/Jayteemighty/Blog-API.git
    ```

2. Navigate to the project directory:

    ```bash
    cd 'blog-api'
    ```

3. Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/macOS
    source venv/Scripts/activate  # For Windows
    ```

4. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

**PostgreSQL Setup:**

1. Install PostgreSQL:

    Follow the instructions on the [PostgreSQL download page](https://www.postgresql.org/download/) for your operating system.

2. Create a new PostgreSQL database and user:

    Open the PostgreSQL command line interface (psql) or use a GUI tool like pgAdmin.

    ```bash
    psql -U postgres
    ```

    Create a new database:

    ```sql
    CREATE DATABASE blogapi_db;
    ```

    Create a new user:

    ```sql
    CREATE USER blogapi_user WITH PASSWORD 'your_password';
    ```

    Grant privileges to the user:

    ```sql
    GRANT ALL PRIVILEGES ON DATABASE blogapi_db TO blogapi_user;
    ```

3. Update your `.env` file (or `settings.py`) with your PostgreSQL database credentials:

    ```env
    # .env file

    DATABASE_URL=postgres://blogapi_user:your_password@localhost:5432/blogapi_db
    ```

    If you're using `settings.py` directly:

    ```python
    # config/settings.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'blogapi_db',
            'USER': 'blogapi_user',
            'PASSWORD': 'your_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

**Development Setup:**

1. Run database migrations:

    ```bash
    python manage.py migrate
    ```

2. Create a superuser account (for initial admin access):

    ```bash
    python manage.py createsuperuser
    ```

3. Start the development server:

    ```bash
    python manage.py runserver
    ```

4. Access Swagger documentation on the development server:

    ```bash
    http://127.0.0.1:8000/docs/
    ```

**Additional Notes:**

* This project uses a `.env` file for environment variables (database connection, etc.). Configure this file locally following the `.env.example` template.
