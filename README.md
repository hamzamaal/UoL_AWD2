# MindTopia -- Learning Management System

## Project Overview

MindTopia is a web-based Learning Management System (LMS) developed
using the Django framework. The platform allows students and teachers to
interact in an online learning environment that supports course
management, quizzes, discussion forums, and user profiles.

The system demonstrates core full-stack web development concepts
including user authentication, role-based access control, database
modelling, and REST API integration.

This project was developed as part of the **UoL AWD2 coursework**.

------------------------------------------------------------------------

# Technologies Used

-   Python
-   Django
-   Django REST Framework
-   Bootstrap
-   HTML
-   CSS
-   SQLite
-   Pillow (Image Processing)
-   Django Crispy Forms

------------------------------------------------------------------------

# Project Structure

    UoL_AWD2/
    │
    ├── MindTopia/
    │   ├── manage.py
    │   ├── requirements.txt
    │   ├── db.sqlite3
    │
    │   ├── MindLMS/        # Django project configuration
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   ├── asgi.py
    │   │   └── wsgi.py
    │
    │   ├── accounts/       # User registration and profiles
    │   ├── courses/        # Course management
    │   ├── forum/          # Discussion forums
    │   ├── quiz/           # Quiz system
    │   ├── quizapi/        # REST API functionality
    │   ├── instructors/    # Teacher related features
    │   ├── donate/         # Donation functionality
    │   ├── feedback/       # Feedback submission
    │   ├── core/           # Core views and templates
    │
    │   ├── static/         # Static files (CSS, JS)
    │   ├── media/          # Uploaded images
    │   └── templates/      # Global templates

------------------------------------------------------------------------

# Features

## User Authentication

-   User registration
-   Login and logout
-   Profile management

## Role-Based Access

Users can be assigned one of two roles:

-   **Student**
    -   Register for courses
    -   Participate in quizzes
    -   View and update profile
    -   Participate in discussions
-   **Teacher**
    -   View student information
    -   Access teacher dashboard

## User Profiles

Each user has a custom profile containing:

-   Profile image
-   Bio
-   Location
-   Date of birth
-   Status updates

## Course Management

Students can register for courses through a many-to-many relationship
between users and courses.

## Quiz System

The platform includes a quiz module that allows students to take
assessments.

## Forum System

Users can participate in discussion forums related to courses.

## REST API

The project integrates **Django REST Framework** to expose data via API
endpoints.

Example serializers:

-   `UserSerializer`
-   `UserProfileSerializer`

------------------------------------------------------------------------

# Installation Guide

## 1. Clone the Repository

``` bash
git clone <repository-url>
cd UoL_AWD2
```

------------------------------------------------------------------------

## 2. Create Virtual Environment

``` bash
python -m venv venv
```

Activate the environment:

### Mac / Linux

``` bash
source venv/bin/activate
```

### Windows

``` bash
venv\Scripts\activate
```

------------------------------------------------------------------------

## 3. Install Dependencies

``` bash
pip install -r MindTopia/requirements.txt
```

------------------------------------------------------------------------

## 4. Apply Database Migrations

``` bash
cd MindTopia
python manage.py migrate
```

------------------------------------------------------------------------

## 5. Create Superuser

``` bash
python manage.py createsuperuser
```

------------------------------------------------------------------------

## 6. Run Development Server

``` bash
python manage.py runserver
```

Open the application in the browser:

    http://127.0.0.1:8000

Admin interface:

    http://127.0.0.1:8000/admin

------------------------------------------------------------------------

# Static and Media Files

Static files such as CSS and JavaScript are stored in:

    MindTopia/static/

User uploaded files such as profile images are stored in:

    MindTopia/media/

------------------------------------------------------------------------

# Key Dependencies

Major dependencies used in this project include:

-   Django
-   djangorestframework
-   Pillow
-   django-crispy-forms
-   crispy-bootstrap5

------------------------------------------------------------------------

# Security Notes

For development purposes the following settings are enabled:

    DEBUG = True
    ALLOWED_HOSTS = ["*"]

For production deployment these values should be changed.

------------------------------------------------------------------------

# Future Improvements

Potential future improvements include:

-   Real-time messaging between students and teachers
-   Course progress tracking
-   Assignment submission functionality
-   Notifications system
-   Containerized deployment using Docker
-   Redis integration for Django Channels

------------------------------------------------------------------------

# Author

Developed as part of the **UoL AWD2 coursework project**.
