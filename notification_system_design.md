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

# Stage 2 – Database Design and Storage Strategy

## Database Recommendation

I recommend PostgreSQL as the primary database for storing notifications.

### Reasons

1. ACID compliance ensures reliable transactions.
2. Supports indexing and query optimization.
3. Handles millions of records efficiently.
4. Supports partitioning and replication.
5. Easy integration with REST APIs.

---

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
```

### Notifications Table

```sql
CREATE TABLE notifications (
    notification_id UUID PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(20) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
);
```

---

## Entity Relationship

One User can have many Notifications.

```text
USERS
------
user_id (PK)
name
email

       1
       |
       |
       N

NOTIFICATIONS
--------------
notification_id (PK)
user_id (FK)
title
message
notification_type
is_read
created_at
```

---

## SQL Queries

### Insert Notification

```sql
INSERT INTO notifications
(notification_id,user_id,title,message,notification_type)
VALUES
(uuid_generate_v4(),
'USR001',
'Placement Opportunity',
'TCS hiring drive starts tomorrow.',
'Placement');
```

### Fetch User Notifications

```sql
SELECT *
FROM notifications
WHERE user_id='USR001'
ORDER BY created_at DESC;
```

### Fetch Unread Notifications

```sql
SELECT *
FROM notifications
WHERE user_id='USR001'
AND is_read=FALSE
ORDER BY created_at DESC;
```

### Mark Notification Read

```sql
UPDATE notifications
SET is_read=TRUE
WHERE notification_id='NOT001';
```

### Delete Notification

```sql
DELETE FROM notifications
WHERE notification_id='NOT001';
```

---

## Challenges at Scale

Current size:

- 50,000 students
- 5,000,000 notifications

Potential issues:

### Slow Queries

Large table scans increase response time.

### High Storage Consumption

Millions of notifications increase table size.

### Increased DB Load

Frequent notification fetches overload the database.

### Real-Time Delivery Bottlenecks

Mass notification delivery becomes difficult.

---

## Solutions

### Indexing

```sql
CREATE INDEX idx_user_read_created
ON notifications(user_id,is_read,created_at);
```

### Table Partitioning

Partition notifications monthly.

Example:

```text
notifications_2026_01
notifications_2026_02
notifications_2026_03
```

### Redis Caching

Store frequently accessed unread counts.

### Read Replicas

Separate read and write workloads.

### Message Queue

Use Kafka or RabbitMQ for notification delivery.

---

## NoSQL Alternative

MongoDB can also be used.

### Document Structure

```json
{
  "_id":"NOT001",
  "userId":"USR001",
  "title":"Placement Opportunity",
  "message":"TCS hiring drive starts tomorrow.",
  "notificationType":"Placement",
  "isRead":false,
  "createdAt":"2026-06-09T10:00:00Z"
}
```

### Fetch Notifications

```javascript
db.notifications.find({
    userId:"USR001"
})
```

### Mark Read

```javascript
db.notifications.updateOne(
  {_id:"NOT001"},
  {$set:{isRead:true}}
)
```

---

## Conclusion

PostgreSQL with indexing, partitioning, caching, and message queues provides a scalable solution capable of handling millions of notifications while maintaining fast response times.

# Stage 3 – Query Optimization and Indexing

## Given Query

```sql
SELECT *
FROM notifications
WHERE studentID = 1042
AND isRead = false
ORDER BY createdAt ASC;
```

---

## Is The Query Correct?

Yes.

The query correctly retrieves all unread notifications of student 1042 and sorts them by creation time.

---

## Why Is It Slow?

Current data size:

- 50,000 students
- 5,000,000 notifications

Without proper indexing, the database performs a full table scan.

Complexity:

```text
O(N)
```

where N = total notifications.

The database may examine millions of rows before finding matching records.

---

## Improvements

Avoid:

```sql
SELECT *
```

Use only required columns.

```sql
SELECT notification_id,
title,
message,
createdAt
FROM notifications
WHERE studentID=1042
AND isRead=false
ORDER BY createdAt ASC;
```

---

## Recommended Index

```sql
CREATE INDEX idx_student_read_created
ON notifications(studentID,isRead,createdAt);
```

Benefits:

- Faster filtering
- Faster sorting
- Reduced disk reads

Expected complexity:

```text
O(log N)
```

---

## Should We Add Indexes On Every Column?

No.

Adding indexes on every column is bad practice.

### Problems

1. Increased storage usage.
2. Slower INSERT operations.
3. Slower UPDATE operations.
4. More index maintenance.

Indexes should only be created on frequently searched and sorted columns.

---

## Query To Find Students Receiving Placement Notifications In Last 7 Days

```sql
SELECT DISTINCT studentID
FROM notifications
WHERE notificationType='Placement'
AND createdAt >= NOW() - INTERVAL '7 DAY';
```

---

## Additional Optimization Techniques

1. Pagination
2. Partitioning
3. Redis Cache
4. Read Replicas
5. Materialized Views

---

## Conclusion

A composite index on studentID, isRead, and createdAt significantly improves query performance while avoiding unnecessary indexing overhead.

Added Stage 3 Query Optimization

# Stage 4 – Reducing Database Load

## Problem

Notifications are fetched on every page load.

Consequences:

- Increased DB traffic
- Slow page response
- Higher infrastructure cost
- Poor user experience

---

## Solution 1 – Redis Cache

Store frequently accessed notifications in Redis.

Flow:

```text
User
 ↓
Redis Cache
 ↓
Database (only if cache miss)
```

Benefits:

- Millisecond response time
- Reduced DB load

Tradeoff:

- Additional infrastructure
- Cache invalidation complexity

---

## Solution 2 – Pagination

Instead of loading all notifications:

```text
?page=1&limit=20
```

Benefits:

- Smaller responses
- Faster API performance

Tradeoff:

- Requires multiple requests

---

## Solution 3 – Lazy Loading

Load notifications only when notification panel opens.

Benefits:

- Reduced unnecessary requests

Tradeoff:

- Slight delay when opening notifications

---

## Solution 4 – Unread Count API

Fetch only unread count initially.

```http
GET /users/{id}/notifications/unread-count
```

Benefits:

- Very small payload

Tradeoff:

- Additional endpoint maintenance

---

## Solution 5 – WebSockets

Push notifications in real time.

Benefits:

- No polling
- Reduced API requests

Tradeoff:

- Persistent connection management

---

## Recommended Architecture

```text
Client
 ↓
Redis
 ↓
Notification API
 ↓
PostgreSQL

WebSocket Server
 ↓
Real-Time Updates
```

---

## Conclusion

Combining Redis caching, pagination, unread-count APIs, lazy loading, and WebSockets provides the best balance between performance and scalability.
