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

### Testing Examples

#### Using curl

```bash
# Create user
curl -X POST http://127.0.0.1:8000/user/create \
  -H "Content-Type: application/json" \
  -d '{"username":"javad","password":"1234"}'

# Login
curl -X POST http://127.0.0.1:8000/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"javad","password":"1234"}'

# Get current user
curl -X GET http://127.0.0.1:8000/user/me \
  -H "Authorization: Bearer <JWT_TOKEN>"

# Update user
curl -X PATCH http://127.0.0.1:8000/user/update \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"username":"ali","password":"newpass"}'

# Delete user
curl -X DELETE http://127.0.0.1:8000/user/delete \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

#### Using Python requests

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Login
res = requests.post(f"{BASE_URL}/user/login", json={"username":"javad","password":"1234"})
token = res.json()["data"]["access_token"]

# Get current user
res = requests.get(f"{BASE_URL}/user/me", headers={"Authorization": f"Bearer {token}"})
print(res.json())

# Update user
res = requests.patch(f"{BASE_URL}/user/update", json={"username":"ali"}, headers={"Authorization": f"Bearer {token}"})
print(res.json())

# Delete user
res = requests.delete(f"{BASE_URL}/user/delete", headers={"Authorization": f"Bearer {token}"})
print(res.json())
```