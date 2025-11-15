from .models import CustomUser
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, AllUsersSerializer, UserRoleSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# Create your views here.
# request -> response

def test_hello(request):
    return HttpResponse('Test Hello World!')

class UserRoleUpdate(APIView):
    """
    Allows Admin ('is_staff' superusers) to update roles of existing users by setting 'is_doctor' or 'is_patient' tags to True. Once flags set, signal (accounts/signals.py) automatically creates the corresponding Doctor or Patient profile for that user.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = UserRoleSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  # triggers profile creation via signal
            return Response({"message": "Role updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAccountsList(APIView):
    """
    For testing purposes, verifies registration.
    Only superusers (admin) can call -> isAdminUser automatically checks.
    Returns a list of all the registered users.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = AllUsersSerializer(users, many=True)
        return Response(serializer.data)

class UserRegisterCreate(APIView):
    """
    Registers new users by creating CustomUser object via serializer. 
    Returns a 201 response if successful, 400 otherwise.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginList(TokenObtainPairView):
    """
    Logs returning users back into their profile.
    """
    serializer_class = CustomTokenObtainPairSerializer

class UserLogoutList(APIView):
    """
    Logs the correct user out from their profile.
    """
    permissions = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": "logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "bad token"}, status=status.HTTP_400_BAD_REQUEST)

class DeleteUser(APIView):
    permissions = [IsAuthenticated, IsAdminUser]

    def delete(self, request, target_id):
        user = request.user

        if not user.is_staff:
            return Response("only admin can delete users", status=status.HTTP_403_FORBIDDEN)
        
        try:
            target_user = CustomUser.objects.get(id=target_id)
        except CustomUser.DoesNotExist:
            return Response(f"target user {target_id} not found", status=status.HTTP_404_NOT_FOUND)

        target_user.delete()
        return Response(f"target user {target_id} removed from record")
