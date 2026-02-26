from django.urls import path
from .views import RegisterView, VerifyEmail, pending_users, approve_user, reject_user, reset_user_password, reset_user_password, toggle_user_status, view_user_logs

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify-email/<uidb64>/<token>/', VerifyEmail.as_view()),
    path('admin/pending-users/', pending_users),
    path('admin/approve/<int:user_id>/', approve_user),
    path('admin/reject/<int:user_id>/', reject_user),
    path('admin/toggle-status/<int:user_id>/', toggle_user_status),
    path('admin/reset-password/<int:user_id>/', reset_user_password),
    path('admin/user-logs/<int:user_id>/', view_user_logs),
]