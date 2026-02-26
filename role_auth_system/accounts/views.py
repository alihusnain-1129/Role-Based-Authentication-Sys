from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .serializers import UserRegisterSerializer
from .utils import send_verification_email
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from django.contrib.admin.models import LogEntry



User = get_user_model()

# User Registration
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            try:
                send_verification_email(user, request)
            except Exception as e:
                print("Email sending failed:", e)  # logs the error
                # return success message anyway
                return Response({"message": "User registered, but email failed to send."}, status=201)
            return Response({"message": "User registered. Verify your email first."}, status=201)
        return Response(serializer.errors, status=400)

# Email verification
class VerifyEmail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            return Response({"error": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"success": "Email verified successfully. Wait for admin approval."})
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

# Admin Endpoints
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def pending_users(request):
    users = User.objects.filter(is_active=True, is_approved=False)
    data = [{"id": u.id, "username": u.username, "email": u.email, "role": u.role} for u in users]
    return Response(data)

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def approve_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_approved = True
        user.save()
        return Response({"success": "User approved"})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def reject_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
        return Response({"success": "User rejected"})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    

@api_view(['POST'])
@permission_classes([IsAdminUser])
def toggle_user_status(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active  # toggles status
        user.save()
        status = "activated" if user.is_active else "deactivated"
        return Response({"success": f"User {status} successfully"})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    

@api_view(['POST'])
@permission_classes([IsAdminUser])
def reset_user_password(request, user_id):
    """
    Admin resets user password
    Body: {"new_password": "Strong@123"}
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    new_password = request.data.get("new_password")
    if not new_password:
        return Response({"error": "New password is required"}, status=400)

    user.password = make_password(new_password)
    user.save()
    return Response({"success": "Password reset successfully"})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def view_user_logs(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    logs = LogEntry.objects.filter(user_id=user_id).values(
        'action_time', 'action_flag', 'change_message', 'content_type_id'
    )
    return Response({"logs": list(logs)})