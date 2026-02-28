
# **URL Shortener – Django REST Framework**

A simple, scalable URL shortener built using Django + Django REST Framework.

This service allows users to:

* Create short URLs for long URLs

* Optionally provide a custom alias

* Optionally set an expiration time

* Redirect users using the short URL

* Automatically invalidate expired URLs



## Tech Stack

Python 3.11

Django 5.x

Django REST Framework

PostgreSQL


## Core Concepts
| Entities | Entity	Description |
|--|--|
| ShortURL | Maps a short code to a long URL |
|short_code	|Unique identifier used in the short URL|
| long_url|	Original URL  |
|expires_at|	Timestamp after which the short URL is invalid|




## API Overview
|Method| Endpoint | Purpose |
|--|--|--|
| POST |  /urls/|Create a short URL
|GET|{short_code}| Redirect to long URL


## Base URL
http://127.0.0.1:8000
## 1. Create Short URL
**Endpoint**
```
POST /urls/
```
**Headers**
```Content-Type: application/json```

## 1.1 Create with long URL only (default expiration)
### Request
{
  "long_url": "https://example.com"
}
### Behavior

Generates a random short code

Applies default expiration (DEFAULT_URL_EXPIRATION_DAYS)

Stores entry in DB

### Response (201 Created)
{
  "short_url": "http://127.0.0.1:8000/aZ3xP9/",
  "expires_at": "2026-03-29T10:30:00Z"
}

## 1.2 Create with custom alias
### Request
{
  "long_url": "https://example.com",
  "custom_alias": "my-link"
}
### Response (201 Created)
{
  "short_url": "http://127.0.0.1:8000/my-link/",
  "expires_at": "2026-03-29T10:30:00Z"
}
## 1.3 Custom alias already exists
### Request
{
  "long_url": "https://example.com",
  "custom_alias": "my-link"
}
### Response (409 Conflict)
{
  "error": "Custom alias already exists"
}
## 1.4 Create with custom expiration date
### Request
{
  "long_url": "https://example.com",
  "expiration_date": "2026-02-01T12:00:00Z"
}
### Response (201 Created)
{
  "short_url": "http://127.0.0.1:8000/Qx8Lm2/",
  "expires_at": "2026-02-01T12:00:00Z"
}
## 1.5 Invalid long URL
### Request
{
  "long_url": "not-a-url"
}
### Response (400 Bad Request)
{
  "long_url": ["Enter a valid URL."]
}

## 2. Redirect Using Short URL
**Endpoint**
```GET /{short_code}/```

Example:

```GET /my-link/```
## 2.1 Valid and active short URL
### Response
HTTP/1.1 302 Found
Location: https://example.com

Browser automatically follows redirect

No JSON body is returned

## 2.2 Expired short URL
### Response
HTTP/1.1 410 Gone
2.3 Non-existent short code
### Response
HTTP/1.1 404 Not Found
Important Behavior Notes
Redirects do NOT return JSON

This is expected.

Short URLs return HTTP redirects

Browsers follow redirects automatically


### Cleanup of Expired URLs
PostgreSQL cleanup command
```
DELETE FROM urls_shorturl
WHERE expires_at <= NOW();
```
---
Availability > consistency

Multiple short URLs per long URL allowed

No automatic deduplication

Redirects use HTTP 302

---

### Local Development
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Summary

This service implements a correct, HTTP-compliant URL shortener with:

Clear API behavior

Explicit expiration handling

Production-safe cleanup strategy

Scalable design choices

