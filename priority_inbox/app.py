import requests

API_URL = "http://4.224.186.213/evaluation-service/notifications"

response = requests.get(API_URL)
notifications = response.json()

priority_map = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}

for notification in notifications:
    notification["priority_score"] = priority_map.get(
        notification.get("notification_type"),
        0
    )

sorted_notifications = sorted(
    notifications,
    key=lambda x: x["priority_score"],
    reverse=True
)

top10 = sorted_notifications[:10]

print("TOP 10 PRIORITY NOTIFICATIONS")
print("-" * 40)

for notification in top10:
    print(notification)

response = requests.get(API_URL)

# Convert response to JSON
notifications = response.json()

# Priority mapping
priority_map = {
