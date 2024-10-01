# Fitness Center Management System

This is a Flask-based RESTful API for managing a fitness center. It provides endpoints for managing members and their workout sessions.

## Features

- CRUD operations for members
- CRUD operations for workout sessions
- Retrieve workout sessions for specific members

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- MySQL 5.7+ or 8.0+

## Installation

1. Clone the repository:

README.md
git clone https://github.com/yourusername/fitness-center-management.git cd fitness-center-management


2. Create a virtual environment and activate it:

python -m venv venv source venv/bin/activate # On Windows use venv\Scripts\activate


3. Install the required packages:

pip install -r requirements.txt


4. Set up your MySQL database and update the `SQLALCHEMY_DATABASE_URI` in `app.py` with your database credentials.

5. Run the application:

python app.py
