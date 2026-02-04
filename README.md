# FastAPI RESTful User Auth

A **RESTful user management API** with JWT authentication using FastAPI.
Designed with clean architecture, JWT-based authentication, and standardized JSON responses.

---

## Features

- RESTful API design
- JWT authentication (Bearer token)
- User registration & login
- Protected user routes
- Standardized success & error responses
- Environment-based configuration using `.env`

---

## Installation & Running

```bash
git clone https://github.com/DevJavad/RESTful-user-auth.git
cd src
pip install -r requirements.txt
python -m main.py
```

---

## Authentication

All protected endpoints require this header:

```
Authorization: Bearer <ACCESS_TOKEN>
```

---

## API Endpoints Overview

| Endpoint | Method | Auth | Description |
|--------|--------|------|------------|
| `/user/create` | POST | ❌ | Create a new user |
| `/user/login` | POST | ❌ | Login and receive JWT |
| `/user/me` | GET | ✅ | Get current user info |
| `/user/update` | PATCH | ✅ | Update username or password |
| `/user/delete` | DELETE | ✅ | Delete current user |

---

## Endpoint Details

### 🔹 Create User

**POST** `/user/create`

**Body (JSON)**

| Field | Type | Required |
|-----|------|----------|
| username | string | ✅ |
| password | string | ✅ |

**Success Response**
```json
{
  "status": "success",
  "message": "Created a new user",
  "data": {
    "user_id": 1
  }
}
```

**Error Response**
```json
{
  "status": "error",
  "message": "username already exists",
  "error": "EXISTS_USERNAME"
}
```

---

### 🔹 Login User

**POST** `/user/login`

**Body (JSON)**

| Field | Type | Required |
|-----|------|----------|
| username | string | ✅ |
| password | string | ✅ |

**Success Response**
```json
{
  "status": "success",
  "message": "login successful",
  "data": {
    "access_token": "<JWT_TOKEN>",
    "token_type": "bearer"
  }
}
```

---

### 🔹 Get Current User

**GET** `/user/me`  
🔐 Requires Authentication

**Success Response**
```json
{
  "status": "success",
  "message": "current user info",
  "data": {
    "id": 1,
    "username": "javad"
  }
}
```

---

### 🔹 Update User

**PATCH** `/user/update`  
🔐 Requires Authentication

**Body (JSON)** — all fields optional

| Field | Type |
|-----|------|
| username | string |
| password | string |

**Success Response**
```json
{
  "status": "success",
  "message": "user updated successfully"
}
```

---

### 🔹 Delete User

**DELETE** `/user/delete`  
🔐 Requires Authentication

**Success Response**
```json
{
  "status": "success",
  "message": "user deleted successfully"
}
```