# URL Monitoring Service

A scalable backend system built using FastAPI and PostgreSQL to monitor website health, track response times, and maintain uptime logs.

The system periodically checks registered URLs using a background scheduler and stores health statistics for analysis. The project also includes JWT-based authentication, authorization, Dockerized deployment, and concurrent request processing for improved monitoring performance.

---

# Features

* User signup and signin
* JWT-based authentication and authorization
* Add and manage monitored URLs
* Automated background URL health checking
* Response time tracking
* Historical uptime logs
* Concurrent URL monitoring using `ThreadPoolExecutor`
* Dockerized FastAPI and PostgreSQL setup
* AWS EC2 deployment support
* REST APIs with FastAPI Swagger documentation

---

# Tech Stack

## Backend

* Python
* FastAPI
* SQLModel / SQLAlchemy
* PostgreSQL

## Authentication

* JWT (JSON Web Tokens)

## Concurrency

* ThreadPoolExecutor

## Deployment

* Docker
* AWS EC2

---

# Architecture Overview

```text
Client
   ↓
FastAPI Backend
   ↓
Authentication Layer (JWT)
   ↓
Business Logic Layer
   ↓
PostgreSQL Database

Background Scheduler
   ↓
Concurrent URL Health Checks
   ↓
Health Logs Storage
```

---

# Performance Optimization

Initially, URLs were monitored sequentially, causing slow execution for multiple URLs.

The scheduler was optimized using `ThreadPoolExecutor` to perform concurrent network requests.

## Performance Improvement

| Method               | Time for 20 URL checks |
| -------------------- | ---------------------- |
| Sequential Execution | ~35 seconds            |
| Concurrent Execution | ~7 seconds             |

---

# API Endpoints

## Authentication

### Signup

`POST /signup`

### Signin

`POST /signin`

Returns JWT token after successful authentication.

---

## URL Management

### Add URL

`POST /urls`

### Get User URLs

`GET /urls`

---

## Monitoring

### Check URL Status

`POST /check/{url_id}`

### Get URL Statistics

`GET /data/{url_id}`

Returns:

* uptime history
* response times
* recent checks
* status analytics

---

# Authentication & Authorization

The project uses JWT-based authentication.

Protected routes require:

```text
Authorization: Bearer <token>
```

Authorization checks ensure users can only access their own URLs and monitoring data.

---

# Docker Setup

The project is fully containerized using Docker.

Containers:

* FastAPI application container
* PostgreSQL database container

---

# AWS Deployment

The application was deployed on an AWS EC2 instance using Docker containers.

Deployment includes:

* Dockerized FastAPI backend
* PostgreSQL container
* Environment variable configuration
* Public API access through EC2 networking and security groups

---

# Environment Variables

Example `.env` variables:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
```

---

# Running the Project

## Clone Repository

```bash
git clone <repository_url>
cd <repository_name>
```

## Run PostgreSQL Container

```bash
docker run -d \
--name postgres-db \
-p 8100:5432 \
--env-file .env \
-v postgres_data:/var/lib/postgresql \
postgres:16
```

## Build FastAPI Container

```bash
docker build -t url-monitor-service .
```

## Run FastAPI Container

```bash
docker run -d \
--name fastapi-app \
-p 8000:8000 \
--env-file .env \
url-monitor-service
```

---

# Future Improvements

Potential future enhancements:

* Async-based monitoring architecture
* Redis-based task queues
* Email/Slack alerts for downtime
* Grafana monitoring dashboards
* CI/CD pipeline integration
* Reverse proxy with Nginx

---

# Learning Outcomes

This project helped build practical understanding of:

* Backend API development
* Database modeling
* Authentication and authorization
* Concurrent execution
* Background scheduling
* Docker containerization
* Cloud deployment using AWS EC2
* Production-style backend architecture

---

# Author

Dwijit Dasari
