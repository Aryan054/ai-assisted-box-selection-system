# AI-Assisted Box Selection System

## Overview

The **AI-Assisted Box Selection System** is a Django REST Framework application that recommends the most suitable shipping box for customer orders based on product dimensions and weight.

The system calculates the required package dimensions, evaluates all available shipping boxes, and selects the smallest box that can safely accommodate the order while respecting weight constraints.

This project was developed as part of a backend engineering assignment and follows clean architecture principles by separating business logic into a dedicated service layer.

---

## Features

* Product management
* Shipping box management
* Order management
* Automatic box recommendation
* RESTful API built with Django REST Framework
* Input validation
* Error handling with meaningful HTTP status codes
* Service layer architecture
* Unit and API tests
* Django Admin support

---

## Tech Stack

* Python <Python Version>
* Django <Django Version>
* Django REST Framework
* SQLite (Development)
* PostgreSQL (Optional)
* Pytest / Django Test Framework (if applicable)

---

## Project Architecture

```text
Client
    │
    ▼
REST API
    │
    ▼
Serializers
    │
    ▼
Service Layer
    │
    ▼
Models
    │
    ▼
Database
```

---

# Installation

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

```bash
cd <PROJECT_DIRECTORY>
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=<YOUR_SECRET_KEY>

DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost
```

Add any additional environment variables required by your project.

---

## 5. Apply migrations

```bash
python manage.py migrate
```

---

## 6. Load sample data (Optional)

```bash
python manage.py loaddata sample_data.json
```

---

## 7. Create an admin user

```bash
python manage.py createsuperuser
```

---

## 8. Run the development server

```bash
python manage.py runserver
```

Server:

```
http://127.0.0.1:8000/
```

Admin:

```
http://127.0.0.1:8000/admin/
```

---

# API Documentation

## Base URL

```
http://127.0.0.1:8000/api/
```

---

## Recommend Shipping Box

### Endpoint

```
POST /recommend-box/
```

### Request

```json
{
    "order_id": 1
}
```

---

### Successful Response

```json
{
    "success": true,
    "order_id": 1,
    "selected_box": "Medium Box",
    "total_weight": "3.50",
    "box_dimensions": {
        "length": "40.00",
        "width": "30.00",
        "height": "20.00"
    },
    "message": "Recommended box selected successfully."
}
```

---

### Error Response

```json
{
    "success": false,
    "message": "No suitable box found."
}
```

---

## HTTP Status Codes

| Status | Description                           |
| ------ | ------------------------------------- |
| 200    | Recommendation generated successfully |
| 400    | Validation error                      |
| 404    | Resource not found                    |
| 422    | No suitable box available             |
| 500    | Internal server error                 |

---

# Example API Requests

## cURL

```bash
curl -X POST \
http://127.0.0.1:8000/api/recommend-box/ \
-H "Content-Type: application/json" \
-d '{
    "order_id":1
}'
```

---

## HTTPie

```bash
http POST http://127.0.0.1:8000/api/recommend-box/ order_id:=1
```

---

## Postman

* Method: **POST**
* URL:

```
http://127.0.0.1:8000/api/recommend-box/
```

Headers:

```
Content-Type: application/json
```

Body:

```json
{
    "order_id":1
}
```

---

# Running Tests

Run all tests:

```bash
python manage.py test
```

Run model tests:

```bash
python manage.py test shipping.tests.test_models
```

Run service tests:

```bash
python manage.py test shipping.tests.test_services
```

Run API tests:

```bash
python manage.py test shipping.tests.test_api
```

Generate coverage report (optional):

```bash
coverage run manage.py test

coverage report

coverage html
```

---

# Project Structure

```text
project/
│
├── config/
│
├── shipping/
│   ├── models.py
│   ├── serializers.py
│   ├── services/
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests/
│   └── fixtures/
│
├── requirements.txt
├── manage.py
└── README.md
```

---

# Design Decisions

* Business logic is isolated in a dedicated service layer.
* Serializers are responsible for request validation.
* Views remain thin and handle only HTTP concerns.
* Models represent the database schema.
* Unit tests cover models, services, and API endpoints.

---

# Future Improvements

* Support advanced 3D bin-packing algorithms.
* Add authentication and authorization.
* Generate OpenAPI/Swagger documentation.
* Add Docker support.
* Add CI/CD using GitHub Actions.
* Improve packing efficiency using optimization techniques.
* Support multiple warehouses.
* Add asynchronous processing with Celery.
* Add caching with Redis.
* Support multiple shipping providers.

---

# Performance Considerations

* Database queries use `select_related()` where appropriate.
* Filtering is performed in the database when possible.
* Business logic is separated from the API layer.
* Recommendation algorithm runs in approximately **O(n + m)** time, where:

  * **n** = number of order items
  * **m** = number of available boxes

---

# Assumptions

* All product dimensions are stored in the same unit.
* All weights use the same measurement unit.
* Products are stacked using the project's chosen packing strategy.
* The smallest valid box is selected when multiple boxes qualify.

---

# Author

**Name:** <YOUR_NAME>

**Email:** <YOUR_EMAIL>

**GitHub:** <YOUR_GITHUB_PROFILE>

**LinkedIn:** <YOUR_LINKEDIN_PROFILE>

---

# License

This project is licensed under the **<LICENSE_NAME>** License.

Add a `LICENSE` file to the repository if you intend to publish it as open source.
