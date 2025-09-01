🎬 Movies Backend (Django + DRF)

This is the backend for the Movies application.
It provides a REST API for managing movies 🎥 and reviews 💬, with authentication handled via tokens.

🚀 Tech Stack

Python 3.11+

Django
 (v5+)

Django REST Framework (DRF)

django-cors-headers
 for CORS support

Pillow
 for image uploads

📂 Project Structure
movies-server/
 ├── moviesweb/              # Django project root
 │    ├── settings.py        # Main settings (API, apps, CORS, etc.)
 │    ├── urls.py            # API routes
 │    ├── wsgi.py / asgi.py  # Deployment entrypoints
 │    └── ...
 ├── movies/                 # Movies app (models, views, serializers)
 ├── reviews/                # Reviews app (models, views, serializers)
 ├── manage.py
 └── requirements.txt

⚙️ Installation
1. Clone and enter the backend folder
git clone <REPO_URL>
cd movies-server/moviesweb

2. Create and activate a virtual environment

On Windows (PowerShell):

python -m venv venv
.\venv\Scripts\activate


On Linux/Mac:

python -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt


If you don’t have a requirements.txt, install manually:

pip install "Django>=5.0,<6.0" djangorestframework django-cors-headers Pillow

4. Run migrations
python manage.py migrate

5. Create a superuser (admin)
python manage.py createsuperuser

6. Run development server
python manage.py runserver


Server will start at:
👉 http://127.0.0.1:8000

🔐 Authentication

Users can register and login through endpoints:

POST /auth/register/

POST /auth/login/

Authentication is handled with Token Auth.

Include the token in headers for protected endpoints:

Authorization: Token <your_token>

📝 Main Endpoints
Movies

GET /movies/ → list all movies

POST /movies/ → create a movie (requires token)

GET /movies/:id/ → retrieve single movie

PATCH /movies/:id/ → update movie (requires token)

DELETE /movies/:id/ → delete movie (requires token)

Reviews

GET /movies/:movieId/reviews/ → list reviews for a movie

POST /movies/:movieId/reviews/ → create review (requires token)

PATCH /reviews/:id/ → update review (requires token)

DELETE /reviews/:id/ → delete review (requires token)

🌍 CORS Setup

In settings.py:

INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
    'movies',
    'reviews',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOW_ALL_ORIGINS = True  # development only

✅ Next Steps

Configure JWT with djangorestframework-simplejwt (optional).

Deploy to production using Gunicorn/Uvicorn + Nginx or on Docker.

Replace CORS_ALLOW_ALL_ORIGINS = True with a whitelist of domains for security.

Would you like me to merge this backend README with the frontend README so you have one unified full-stack README (client + server) in a single document?
