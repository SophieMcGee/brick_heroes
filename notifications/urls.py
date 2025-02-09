from django.urls import path
from .views import admin_notifications, user_notifications, approve_review, delete_review

urlpatterns = [
    path("admin/notifications/", admin_notifications, name="admin_notifications"),
    path("notifications/", user_notifications, name="user_notifications"),
    path("admin/notifications/approve-review/<int:review_id>/", approve_review, name="approve_review"),
    path("admin/notifications/delete-review/<int:review_id>/", delete_review, name="delete_review"),
]