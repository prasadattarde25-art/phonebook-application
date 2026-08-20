# Phonebook Application

A production-style full-stack Phonebook Application built using **Vue.js 3, FastAPI, PostgreSQL, SQLAlchemy, Axios, Docker, and Docker Compose**.

The application provides a complete contact-management workflow with RESTful CRUD APIs, persistent PostgreSQL storage, frontend-backend integration, validation, API documentation, and containerized development.

---

##   Project Demo

▶️ **[Watch the Complete Project Demo](https://www.youtube.com/watch?v=6afFIaAIQRk)**

The demo covers:
- Application UI
- CRUD operations
- Search and pagination
- REST APIs
- Swagger / OpenAPI
- Docker
- ngrok public URL

---

## 1. Project Overview

The application is designed as a three-tier architecture:

```text
                    USER
                      │
                      ▼
              ┌───────────────┐
              │   Vue.js 3    │
              │   Frontend    │
              └───────┬───────┘
                      │
                Axios / HTTP
                      │
                      ▼
              ┌───────────────┐
              │    FastAPI    │
              │    Backend    │
              └───────┬───────┘
                      │
                  SQLAlchemy
                      │
                      ▼
              ┌───────────────┐
              │  PostgreSQL   │
              │    Database   │
              └───────────────┘
```

All services are containerized and managed using **Docker Compose**.

---

# 2. Business Objective

The goal of the application is to provide a simple and reliable system for managing contact information.

Users can:

* Create contacts
* View all contacts
* View individual contact details
* Update existing contacts
* Delete contacts
* Persist contact information in PostgreSQL

The project demonstrates a complete **Frontend → REST API → Database** workflow.

---

# 3. Technology Stack

| Layer             | Technology        | Purpose                        |
| ----------------- | ----------------- | ------------------------------ |
| Frontend          | Vue.js 3          | User interface                 |
| Routing           | Vue Router        | Client-side navigation         |
| HTTP Client       | Axios             | Frontend-backend communication |
| Backend           | FastAPI           | REST API development           |
| Language          | Python            | Backend implementation         |
| ORM               | SQLAlchemy        | Database interaction           |
| Database          | PostgreSQL        | Persistent data storage        |
| API Documentation | Swagger / OpenAPI | API testing and documentation  |
| Containerization  | Docker            | Application isolation          |
| Orchestration     | Docker Compose    | Multi-service management       |
| Version Control   | Git               | Source-code management         |

---

# 4. Core Features

## Contact Management

The application supports complete CRUD operations:

* **Create** a new contact
* **Read** all contacts
* **Read** individual contact details
* **Update** contact information
* **Delete** contacts with confirmation

## Contact Information

Each contact contains:

```text
ID
Name
Phone Number
Email
Address
Created Timestamp
```

## Frontend

The Vue.js application provides:

* Contact list
* Contact detail page
* Create contact form
* Update contact functionality
* Delete confirmation
* Client-side routing
* Axios API integration

## Backend

The FastAPI backend provides:

* RESTful API
* CRUD operations
* Request validation
* SQLAlchemy integration
* PostgreSQL connectivity
* Swagger/OpenAPI documentation

---

# 5. REST API Design

| Method | Endpoint         | Purpose                     |
| ------ | ---------------- | --------------------------- |
| GET    | `/contacts/`     | Retrieve all contacts       |
| POST   | `/contacts/`     | Create a contact            |
| GET    | `/contacts/{id}` | Retrieve a specific contact |
| PUT    | `/contacts/{id}` | Update a contact            |
| DELETE | `/contacts/{id}` | Delete a contact            |

### API Documentation

After starting the application:

```text
http://localhost:8000/docs
```

OpenAPI specification:

```text
http://localhost:8000/openapi.json
```

Swagger UI can be used to test the APIs without requiring an external API client.

---

# 6. Project Architecture

```text
Phonebook Application
│
├── Frontend
│   └── Vue.js 3
│       ├── Components
│       ├── Router
│       └── Axios
│
├── Backend
│   └── FastAPI
│       ├── Routes
│       ├── Schemas
│       ├── Models
│       └── Database Layer
│
└── Database
    └── PostgreSQL
        └── Contact Data
```

### Request Flow

For example, when a user creates a contact:

```text
User
  │
  ▼
Vue.js Form
  │
  ▼
Axios
  │
  ▼
POST /contacts/
  │
  ▼
FastAPI
  │
  ▼
Request Validation
  │
  ▼
SQLAlchemy
  │
  ▼
PostgreSQL
  │
  ▼
Response
  │
  ▼
Vue.js UI
```

This separation keeps the frontend, business/API layer, and database responsibilities independent.

---

# 7. Project Structure

```text
Phonebook-app/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ContactList.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── App.vue
│   │   ├── ContactDetail.vue
│   │   ├── main.js
│   │   └── style.css
│   │
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

---

# 8. Docker Architecture

Docker Compose manages three independent services:

```text
                    Docker Compose
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
     Frontend          Backend         Database
     Vue.js            FastAPI        PostgreSQL
     :5173             :8000          :5432
```

### Services

| Service  | Technology | Port |
| -------- | ---------- | ---- |
| frontend | Vue.js     | 5173 |
| backend  | FastAPI    | 8000 |
| db       | PostgreSQL | 5432 |

The backend communicates with PostgreSQL using the Docker Compose service name:

```text
db
```

This allows services to communicate through the Docker Compose network without depending on `localhost` between containers.

---
---


# 9. Environment Configuration

Database configuration is provided through environment variables.

Example:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=YOUR_PASSWORD
POSTGRES_DB=phonebook
```

Sensitive credentials should never be committed to Git.

The `.env` file should remain local, while `.env.example` can be committed as a template.

---

# 10. Prerequisites

Install:

* Docker Desktop
* Git
* Node.js
* Python 3.11+

Verify Docker:

```powershell
docker --version
```

Verify Docker Compose:

```powershell
docker compose version
```

---

# 11. Run the Application

## Step 1 — Open the project

```powershell
cd Phonebook-app
```

Verify that the project contains:

```text
docker-compose.yml
backend/
frontend/
.env
README.md
```

## Step 2 — Start Docker Desktop

Make sure Docker Desktop is running.

## Step 3 — Build and start all services

```powershell
docker compose up -d --build
```

This command:

1. Builds the frontend image
2. Builds the backend image
3. Starts PostgreSQL
4. Creates the Docker network
5. Starts all application services

## Step 4 — Verify services

```powershell
docker compose ps
```

Expected services:

```text
phonebook-frontend
phonebook-backend
phonebook-db
```

All services should show a running/healthy state according to the configured Docker health checks.

---

# 12. Application URLs

### Frontend

```text
http://localhost:5173
```

### Backend

```text
http://localhost:8000
```

### Swagger API Documentation

```text
http://localhost:8000/docs
```

### OpenAPI Specification

```text
http://localhost:8000/openapi.json
```

---

---

# 13. Public Access with ngrok

For demonstration and testing purposes, the Phonebook Application can be exposed to the internet using **ngrok**.

ngrok creates a secure public tunnel to the locally running application and provides a public HTTPS URL.

### Start ngrok

After starting the application, run:

```powershell

ngrok http 5173
-----

For demonstration purposes, the Phonebook Application is currently accessible through the following public URL:

🔗 **[Open Phonebook Application](https://quarry-bankroll-juicy.ngrok-free.dev/)**

> **Note:** This is a temporary ngrok URL and is accessible only while the ngrok tunnel is running. The URL may change when the tunnel is restarted.

-----

# 13. API Testing

The REST APIs can be tested through Swagger UI.

Open:

```text
http://localhost:8000/docs
```

### Create Contact

```http
POST /contacts/
```

Example request:

```json
{
  "name": "Rahul Sharma",
  "phone_number": "+919876543210",
  "email": "rahul@gmail.com",
  "address": "Mumbai"
}
```

### Retrieve Contacts

```http
GET /contacts/
```

### Retrieve Contact

```http
GET /contacts/{id}
```

### Update Contact

```http
PUT /contacts/{id}
```

### Delete Contact

```http
DELETE /contacts/{id}
```

---

# 14. End-to-End Testing

The application should be tested from both the API and UI layers.

### Create Contact

1. Open the frontend.
2. Enter contact information.
3. Submit the form.
4. Verify that the contact appears in the contact list.
5. Verify that the data is persisted in PostgreSQL.

### View Contact

1. Select a contact.
2. Open the detail page.
3. Verify ID, name, phone number, email, and address.

### Update Contact

1. Open an existing contact.
2. Select Update.
3. Modify the information.
4. Save the changes.
5. Verify the updated data.

### Delete Contact

1. Select Delete.
2. Confirm the deletion.
3. Verify that the contact is removed from the UI and database.

---

# 15. Docker Troubleshooting

Check running containers:

```powershell
docker compose ps
```

View backend logs:

```powershell
docker compose logs backend
```

View frontend logs:

```powershell
docker compose logs frontend
```

View database logs:

```powershell
docker compose logs db
```

Follow backend logs in real time:

```powershell
docker compose logs -f backend
```

---

# 16. Database Persistence

PostgreSQL uses a Docker named volume for persistent storage.

```text
PostgreSQL Container
        │
        ▼
  Docker Volume
        │
        ▼
Persistent Contact Data
```

Restart services:

```powershell
docker compose restart
```

The previously stored contacts should remain available.

To completely remove containers and database volume:

```powershell
docker compose down -v
```

> **Warning:** Removing the volume deletes the stored PostgreSQL data.

---

# 17. Stopping the Application

Stop the application:

```powershell
docker compose down
```

The Docker images and persistent database volume remain available for the next startup.

---


# 18. Future Enhancements

The current architecture can be extended with:

* Advanced filtering
* Authentication and authorization
* Unit testing
* Integration testing
* Logging
* CI/CD pipeline
* Cloud deployment


These improvements can be introduced without changing the fundamental frontend → backend → database architecture.

---

# 19. Project Deliverables

The project includes:

* Vue.js 3 frontend
* FastAPI backend
* PostgreSQL database
* SQLAlchemy ORM
* Vue Router
* Axios integration
* RESTful CRUD APIs
* Swagger/OpenAPI documentation
* Dockerfile for frontend
* Dockerfile for backend
* Docker Compose configuration
* PostgreSQL persistence
* Environment configuration
* API testing
* End-to-end testing
* Project documentation

---

# 20. Final Architecture

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │   Vue.js 3 UI   │
                  └────────┬────────┘
                           │
                        Axios
                           │
                           ▼
                  ┌─────────────────┐
                  │     FastAPI     │
                  │    REST API     │
                  └────────┬────────┘
                           │
                       SQLAlchemy
                           │
                           ▼
                  ┌─────────────────┐
                  │   PostgreSQL    │
                  │    Database     │
                  └─────────────────┘

                 All services run using
                  Docker + Compose
```

## Conclusion

The Phonebook Application demonstrates a complete full-stack application lifecycle—from frontend interaction and REST API communication to database persistence and containerized deployment.

The project is structured to provide a clean separation between application layers while remaining easy to develop, test, run, and extend.
