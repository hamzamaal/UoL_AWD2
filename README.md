# MindTopia – Learning Management System

## Project Overview

MindTopia is a web-based Learning Management System (LMS) developed using the Django framework. The platform allows students and teachers to interact in an online learning environment that supports course management, quizzes, discussion forums, and user profiles.

The system demonstrates core full-stack web development concepts including user authentication, role-based access control, database modelling, and REST API integration.

This project was developed as part of the **UoL AWD2 coursework**.

---

# Technologies Used

- Python
- Django
- Django REST Framework
- Bootstrap
- HTML
- CSS
- SQLite
- Pillow (Image Processing)
- Django Crispy Forms

---

---

# Features

## User Authentication
- User registration
- Login and logout
- Profile management

## Role-Based Access
Users can be assigned one of two roles:

- **Student**
  - Register for courses
  - Participate in quizzes
  - View and update profile
  - Participate in discussions

- **Teacher**
  - View student information
  - Access teacher dashboard

## User Profiles
Each user has a custom profile containing:

- Profile image
- Bio
- Location
- Date of birth
- Status updates

## Course Management
Students can register for courses through a many-to-many relationship between users and courses.

## Quiz System
The platform includes a quiz module that allows students to take assessments.

## Forum System
Users can participate in discussion forums related to courses.

## REST API
The project integrates **Django REST Framework** to expose data via API endpoints.

Example serializers:

- `UserSerializer`
- `UserProfileSerializer`

---

# Installation Guide

## 1. Clone the Repository

```bash
git clone <repository-url>
cd UoL_AWD2

##2. Create Virtual Environment
python -m venv venv



