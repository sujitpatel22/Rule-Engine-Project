# Rule Engine Project

This is a **Rule Engine** application that allows users to define and evaluate custom rules based on user data. The application provides a simple interface to combine rules, generate an Abstract Syntax Tree (AST), and evaluate user data against these rules.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Combining Rules](#combining-rules)
  - [Evaluating Rules](#evaluating-rules)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)

## Overview

The Rule Engine project provides a flexible way to define business rules for different types of data. The rules can be written in simple condition-based statements (like `age > 30 AND department = 'Sales'`), and the system will build a combined AST from these rules. The user data is then evaluated against the AST to see if it satisfies the rules.

This project is built using **Vue.js** for the frontend and **Django (DRF)** for the backend. The frontend communicates with the backend via REST APIs to combine rules and evaluate them against the user data.

## Features

- Combine multiple rule strings into a unified Abstract Syntax Tree (AST).
- Evaluate user data based on the combined rules.
- Support for basic operators like `AND`, `OR`, `>`, `<`, `>=`, `<=`, `==`, `!=`.
- User-friendly interface to input rules and data.
- Modular and reusable components for rule combination and evaluation.

## Requirements

To run this project, ensure you have the following installed:

### Backend Requirements (Python/Django)

- Python 3.8 or later
- Django 3.0 or later
- Django REST Framework (DRF)
- PostgreSQL (instead of SQLite)
- psycopg2 (PostgreSQL adapter for Python)

To install the dependencies, run the following command:

```bash
pip install -r requirements.txt
```

### Frontend Requirements (Vue.js)

- Node.js 14 or later
- Vue.js 2
- Axios for API calls

## Installation

Follow the steps below to get the project up and running on your local machine:

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sujitpatel22/Rule-Engine-Project.git
   cd Rule-Engine-Project/backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up **PostgreSQL**:

   - Install PostgreSQL on your system if not already installed.
   - Create a PostgreSQL database:
     ```bash
     sudo -u postgres psql
     CREATE DATABASE rule_engine_db;
     CREATE USER rule_user WITH PASSWORD 'password123';
     ALTER ROLE rule_user SET client_encoding TO 'utf8';
     ALTER ROLE rule_user SET default_transaction_isolation TO 'read committed';
     ALTER ROLE rule_user SET timezone TO 'UTC';
     GRANT ALL PRIVILEGES ON DATABASE rule_engine_db TO rule_user;
     ```

5. Update your **Django settings** to use PostgreSQL:

   In `settings.py`, change the `DATABASES` configuration:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'rule_engine_db',
           'USER': 'rule_user',
           'PASSWORD': 'password123',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

6. Run the migrations and start the Django server:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install the necessary node modules:
   ```bash
   npm install / npm update
   ```

3. Run the Vue development server:
   ```bash
   npm run serve
   ```

## Usage

Once both the backend and frontend servers are running, you can access the application in your browser at `http://localhost:8080` (or the default Vue port).

### Combining Rules

1. In the **Rule Combination** section, enter your rule strings in the textarea, with each rule on a new line. For example:

   ```
  - `salary > 50000 OR experience > 5`
  - `age < 25 OR (department = 'Marketing')`
   ```

2. Click **Combine AST**. The rules will be sent to the backend and combined into a unified AST. The combined AST will be displayed on the screen.

### Evaluating Rules

1. In the **Evaluate Rule** section, provide a JSON object representing user data. For example:

   ```json
   {
       "age": 35,
       "department": "Sales",
       "salary": 60000,
       "experience": 5
   }
   ```

2. Click **Evaluate Rule** to check if the user data satisfies the combined rules. The evaluation result will be displayed as either `True` or `False`.

### Example Workflow

- Define two rules:
  - `salary > 50000 OR experience > 5`
  - `age < 25 OR (department = 'Marketing')`

- Combine the rules.
- Pass user data to evaluate it against the rules.

### API Endpoints

The backend provides the following endpoints:

1. **Combine Rules**
   - **Endpoint**: `/combine_rules/`
   - **Method**: `POST`
   - **Payload**:
     ```json
     {
       "rules": [
         "age > 30 AND department = 'Sales'",
         "salary > 50000"
       ]
     }
     ```
   - **Response**:
     ```json
     {
       "ast": {
         "type": "operator",
         "value": "OR",
         "left": { ... },
         "right": { ... }
       },
       "message": "Rules combined successfully."
     }
     ```

2. **Evaluate Rule**
   - **Endpoint**: `/evaluate_rule/`
   - **Method**: `POST`
   - **Payload**:
     ```json
     {
       "ast": { ... }, 
       "data": {
         "age": 35,
         "department": "Sales",
         "salary": 60000
       }
     }
     ```
   - **Response**:
     ```json
     {
       "result": true,
       "message": "Evaluation complete."
     }
     ```

## Technologies Used

- **Frontend**: Vue.js 2, Axios
- **Backend**: Django 3.x, Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Others**: Node.js, NPM
