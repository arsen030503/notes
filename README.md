# API Documentation

This document provides a detailed description of all the API endpoints for the project.

---
http://10.220.99.3:10000 
## **Endpoints**

### **1. Register User**
**Endpoint:** `/register`  
**Method:** `POST`  
**Description:** Registers a new user in the system.

#### Request Body:
```json
{
    "email": "string",
    "password": "string"
}
```

#### Response:
- **Success (200):**
```json
{
    "message": "User registered successfully!"
}
```
- **Failure (400):**
```json
{
    "message": "User already exists."
}
```

---

### **2. Login User**
**Endpoint:** `/login`  
**Method:** `POST`  
**Description:** Authenticates a user with their credentials.

#### Request Body:
```json
{
    "email": "string",
    "password": "string"
}
```

#### Response:
- **Success (200):**
```json
{
    "message": "Login successful!"
}
```
- **Failure (400):**
```json
{
    "message": "Invalid email or password."
}
```

---

### **3. Add Entry with Image**
**Endpoint:** `/add_entry`  
**Method:** `POST`  
**Description:** Adds an entry for the user with an image. The image is sent in Base64 format and saved on the server.

#### Request Body:
```json
{
    "user_id": "integer",
    "image": "string (Base64 encoded image)"
}
```

#### Response:
- **Success (200):**
```json
{
    "message": "Entry added successfully!",
    "image_path": "string (path to the saved image)"
}
```
- **Failure (400):**
```json
{
    "message": "Invalid user ID."
}
```

---

### **4. Get All Entries for a User**
**Endpoint:** `/get_entries/<user_id>`  
**Method:** `GET`  
**Description:** Retrieves all entries for a given user along with image paths.

#### Request Parameters:
- `user_id` (integer): The ID of the user whose entries are to be retrieved.

#### Response:
- **Success (200):**
```json
{
    "entries": [
        {
            "id": "integer",
            "image_path": "string (path to the image)"
        }
    ]
}
```
- **Failure (400):**
```json
{
    "message": "User not found."
}
```

---

## **Additional Information**

- **Database Initialization:**
  - The database and the `uploads` folder are automatically created when the server starts.

- **Image Storage:**
  - Uploaded images are saved in the `uploads` directory on the server.
  - The filename is generated based on the user ID and the entry ID.

---

## **Usage Examples**

### Register User:
```bash
curl -X POST \
-H "Content-Type: application/json" \
-d '{"email": "user@example.com", "password": "password123"}' \
http://localhost:5000/register
```

### Login User:
```bash
curl -X POST \
-H "Content-Type: application/json" \
-d '{"email": "user@example.com", "password": "password123"}' \
http://localhost:5000/login
```

### Add Entry with Image:
```bash
curl -X POST \
-H "Content-Type: application/json" \
-d '{"user_id": 1, "image": "data:image/png;base64,..."}' \
http://localhost:5000/add_entry
```

### Get All Entries for a User:
```bash
curl -X GET \
http://localhost:5000/get_entries/1
```

