from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username')

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['is_doctor', 'is_patient']

    def validate(self, attrs):
        if attrs.get('is_doctor') and attrs.get('is_patient'):
            raise serializers.ValidationError({"two_profiles": "user cannot be both doctor and patient."})
        return attrs

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user. 
    Validates that passwords match (for profile creation). 
    Creates profile via CustomUser model and signals (automatically assign "doctor" or "patient" role).
    """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Adds information about user roles (doctor or patient) to token.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['is_doctor'] = user.is_doctor
        token['is_patient'] = user.is_patient
        return token
    
class UserEmailLookupSerializer(serializers.Serializer):
    target_email = serializers.EmailField()