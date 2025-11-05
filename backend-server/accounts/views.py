from .models import CustomUser, DoctorProfile, PatientProfile
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, AllUsersSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# request -> response

def test_hello(request):
    return HttpResponse('Test Hello World!')

class UserAccountsList(APIView):
    """
    For testing purposes, verifies registration.
    Returns a list of all the registered users.
    """
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


