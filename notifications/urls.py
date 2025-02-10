from django.urls import path
from .views import admin_notifications, user_notifications, approve_review, delete_notification

urlpatterns = [
    path("admin/notifications/", admin_notifications, name="admin_notifications"),
    path("notifications/", user_notifications, name="user_notifications"),
    path("delete/<int:notification_id>/", delete_notification, name="delete_notification"),
    path("admin/notifications/approve-review/<int:review_id>/", approve_review, name="approve_review"),
]