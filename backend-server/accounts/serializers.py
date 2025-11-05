from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username')

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user. 
    Validates that passwords match (for profile creation). 
    Creates profile via CustomUser model and signals (automatically assign "doctor" or "patient" role).
    """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    is_doctor = serializers.BooleanField(default=False)
    is_patient = serializers.BooleanField(default=True) # all new users defaulted as patients -> extra field for veirfying as doctor?

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'password2', 'is_doctor', 'is_patient']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if attrs.get('is_doctor') and attrs.get('is_patient'):
            raise serializers.ValidationError("User cannot be both doctor and patient.")
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