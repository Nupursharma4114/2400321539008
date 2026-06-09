# Stage 1 – Notification System REST API Design

## Objective

Design a notification platform that allows users to receive, view, update, and manage notifications when logged into the application.

---

## Core Actions Supported

1. Create Notification
2. Fetch User Notifications
3. Fetch Notification by ID
4. Mark Notification as Read
5. Mark All Notifications as Read
6. Delete Notification
7. Get Unread Notification Count
8. Real-Time Notification Delivery

---

## Base URL

/api/v1

---

# 1. Create Notification

### Endpoint

POST /notifications

### Headers

Content-Type: application/json

### Request Body

```json
{
  "userId": "USR001",
  "title": "Placement Opportunity",
  "message": "TCS hiring drive starts tomorrow.",
  "notificationType": "Placement"
}
```

### Response (201 Created)

```json
{
  "notificationId": "NOT001",
  "status": "created",
  "createdAt": "2026-06-09T10:00:00Z"
}
```

---

# 2. Get All Notifications For A User

### Endpoint

GET /users/{userId}/notifications

### Query Parameters

```text
?page=1
&limit=20
&status=unread
```

### Response

```json
{
  "total": 2,
  "notifications": [
    {
      "notificationId": "NOT001",
      "title": "Placement Opportunity",
      "message": "TCS hiring drive starts tomorrow.",
      "notificationType": "Placement",
      "isRead": false,
      "createdAt": "2026-06-09T10:00:00Z"
    }
  ]
}
```

---

# 3. Get Notification By ID

### Endpoint

GET /notifications/{notificationId}

### Response

```json
{
  "notificationId": "NOT001",
  "title": "Placement Opportunity",
  "message": "TCS hiring drive starts tomorrow.",
  "notificationType": "Placement",
  "isRead": false
}
```

---

# 4. Mark Notification As Read

### Endpoint

PATCH /notifications/{notificationId}/read

### Request

```json
{
  "isRead": true
}
```

### Response

```json
{
  "message": "Notification marked as read"
}
```

---

# 5. Mark All Notifications As Read

### Endpoint

PATCH /users/{userId}/notifications/read-all

### Response

```json
{
  "message": "All notifications marked as read"
}
```

---

# 6. Delete Notification

### Endpoint

DELETE /notifications/{notificationId}

### Response

```json
{
  "message": "Notification deleted successfully"
}
```

---

# 7. Get Unread Notification Count

### Endpoint

GET /users/{userId}/notifications/unread-count

### Response

```json
{
  "unreadCount": 5
}
```

---

# Standard HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Internal Server Error |

---

# JSON Schema

## Notification Object

```json
{
  "notificationId": "string",
  "userId": "string",
  "title": "string",
  "message": "string",
  "notificationType": "Event | Result | Placement",
  "isRead": "boolean",
  "createdAt": "datetime"
}
```

---

# Real-Time Notification Mechanism

To deliver notifications instantly without refreshing the page, WebSocket technology will be used.

## WebSocket Endpoint

```text
ws://server.com/notifications
```

## Event Payload

```json
{
  "event": "notification.created",
  "data": {
    "notificationId": "NOT001",
    "title": "Placement Opportunity",
    "message": "TCS hiring drive starts tomorrow."
  }
}
```

## Notification Flow

```text
Admin/System
      ↓
Notification Service
      ↓
Database
      ↓
WebSocket Server
      ↓
Connected Users
```

## Benefits Of WebSocket

- Real-time delivery of notifications
- Low latency communication
- Better user experience
- Reduced API polling overhead
- Supports large-scale concurrent users

---

# API Naming Conventions

- Use plural nouns (notifications, users)
- Use standard HTTP methods (GET, POST, PATCH, DELETE)
- Keep endpoints predictable and RESTful
- Return JSON responses consistently
- Use pagination for large datasets

---

# Assumptions

- Users are already authenticated.
- Notifications are linked to a valid user.
- Notification types supported are:
  - Event
  - Result
  - Placement
- System supports both in-app and real-time notifications.

---

# Conclusion

The proposed REST API design provides a scalable, maintainable, and production-ready notification platform. It supports notification creation, retrieval, update, deletion, unread count tracking, and real-time delivery using WebSockets while following RESTful API best practices.
Added Stage 1 Notification System Design
