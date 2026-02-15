# Data Summarization Service

## Overview

This project is a backend service that:

- Fetches news articles from a public API (New York Times)
- Stores them in a PostgreSQL database
- Provides RESTful endpoints to query articles
- Generates AI-powered summaries using OpenAI
- Uses Redis for caching summaries and article lists
- Runs inside Docker containers

The system is built with Django + Django REST Framework.

---

## Architecture

The system follows a clean layered architecture:

Client → API Layer → Service Layer → Database / AI / Cache

### Components

- Django REST API
- PostgreSQL (data storage)
- Redis (caching)
- APScheduler (auto-fetch every 6 hours)
- OpenAI API (AI summaries)
- Docker & Docker Compose

---

## Features

### 1. Automatic Data Fetching

- Fetches articles from NYT API
- Runs every 6 hours
- Prevents duplicate inserts (unique external_id)

### 2. REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/articles/ | List all articles |
| GET | /api/articles/{id}/ | Get article details |
| GET | /api/articles/{id}/summary/ | Get AI summary |
| GET | /health/ | Health Endpoint |

### 3. AI Summarization

- Uses OpenAI `gpt-4o-mini`
- Generates concise summaries (3–4 sentences)
- Includes title, author, section and abstract

### 4. Caching Strategy

- Article list cached in Redis
- Article summaries cached in Redis (TTL: 6 hours)
- Cache invalidation on create/update/delete
- Prevents unnecessary AI calls (cost optimization)

---

## Technologies Used

- Python 3.9
- Django 4.2
- Django REST Framework
- PostgreSQL
- Redis
- OpenAI API
- APScheduler
- Docker & Docker Compose

---

## Running the Project

### 1. Clone Repository

```bash
git clone <repo_url>
cd project_folder
