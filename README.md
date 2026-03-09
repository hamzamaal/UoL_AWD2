
# MindTopia – Online Learning Platform

MindTopia is a web-based learning management platform built with Django.
It allows students and teachers to interact through courses, quizzes, forums, and real-time chat communication.

The application demonstrates a modular Django architecture with REST APIs, real-time communication using WebSockets, and role-based access control.

---

# Features

## User Accounts
- User registration and authentication
- Profile management
- Role-based access (Student / Teacher)

## Courses
- Browse available courses
- Register for courses
- Course detail pages
- Submit course feedback

## Quizzes
- Multiple-choice quizzes linked to courses
- Automatic scoring and result feedback
- Course-specific quiz questions

## Discussion Forum
- Create forum posts
- Update and delete posts
- Comment on posts
- Community discussions between users

## Real-Time Messaging (WebSockets)
The application includes **real-time chat functionality** using **Django Channels and WebSockets**.

Features include:
- Live text chat between students and teachers
- Room-based chat channels
- Instant message broadcasting
- WebSocket connections handled by Django Channels

Users can join a chat room and communicate instantly without refreshing the page.

## Feedback System
- Users can submit structured feedback about the platform and courses.

## Instructor Directory
- Displays available instructors and their information.

## Donation Page
- Authenticated users can access the donation page to support the platform.

## REST API
The platform exposes API endpoints using **Django REST Framework**, including:

- Course list and detail endpoints
- Quiz endpoints
- Course feedback endpoints
- Teacher-only user management endpoints

---

# Technologies Used

- Python 3
- Django 4
- Django REST Framework
- Django Channels (WebSockets)
- Bootstrap 5
- SQLite
- HTML / CSS / JavaScript

---

# Project Structure

MindTopia/
│
├── accounts        # User authentication and profile management
├── core            # Home, about, and general pages
├── courses         # Course management and feedback
├── donate          # Donation page
├── feedback        # Platform feedback forms
├── forum           # Discussion forum and real-time chat
├── instructors     # Instructor directory
├── quiz            # Course quiz functionality
├── quizapi         # Quiz REST API endpoints
│
├── MindLMS         # Main project configuration
│
├── templates       # Shared templates
├── static          # CSS, JavaScript, images
│
└── manage.py

---

# Installation

Clone the repository:

git clone https://github.com/hamzamaal/UoL_AWD2.git
cd UoL_AWD2/MindTopia

Create and activate a virtual environment:

python3.12 -m venv venv312
source venv312/bin/activate

Install dependencies:

pip install -r requirements.txt
pip install daphne

Apply database migrations:

python manage.py migrate
python manage.py makemigrations

Display the Active Database Configuration, checking for issues
python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['NAME'])"

Collect Static Files for Deployment
python manage.py collectstatic --noinput

Create an admin account:

python manage.py createsuperuser

Run the development server:

daphne -b 0.0.0.0 -p 8000 MindLMS.asgi:application

Open the application:

http://127.0.0.1:8000

---

# Running Tests

The project includes automated tests for multiple modules.

Run all tests:

python manage.py test

Run tests for specific modules:

python manage.py test accounts
python manage.py test courses
python manage.py test forum
python manage.py test quiz

---

# Testing Real-Time Chat

To test the WebSocket chat functionality:

1. Start the Django server.
2. Log in with two different users.
3. Open the chat room page in two browser windows.
4. Send messages from one window.
5. Messages should appear instantly in the other window.

This confirms WebSocket real-time communication is functioning correctly.

---

# Advanced Features Demonstrated

The project includes several advanced web development techniques:

- Django Channels WebSocket integration
- Role-based access control
- REST API design with Django REST Framework
- Modular Django application structure
- Automated unit testing

---

# Future Improvements

Possible future enhancements include:

- Video conferencing integration
- File sharing within chat rooms
- Real-time collaborative whiteboards
- Push notifications for course updates
- Improved UI/UX styling

---

# Author

Hamza Maal
University of London – BSc Computer Science
Advanced Web Development
