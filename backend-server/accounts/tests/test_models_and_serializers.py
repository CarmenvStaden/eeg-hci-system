import pytest
from accounts.models import CustomUser, DoctorProfile, PatientProfile
from accounts.serializers import UserRegistrationSerializer, AllUsersSerializer, CustomTokenObtainPairSerializer

@pytest.mark.django_db
def test_custom_user_creation():
    """
    Basic creation of a custom user object.
    """
    user = CustomUser.objects.create_user(
        email = "unitest@gmail.com",
        username = "uni",
        password = "abc123",
    )

    assert user.email == "unitest@gmail.com"
    assert user.check_password("abc123")

@pytest.mark.django_db
def test_user_registration_serializer_valid_default_patient_true():
    """
    Registration of a default patient profile (no booleans passed in body).
    """
    data = {
        "email": "serial@test.com",
        "username": "serializer",
        "password": "pass1234",
        "password2": "pass1234"
    }
    serializer = UserRegistrationSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.email == data["email"]
    assert user.is_patient is True
    assert user.is_doctor is False

@pytest.mark.django_db
def test_user_registration_serializer_valid_doctor_set_true():
    """
    Registration of a doctor profile (is_doctor boolean passed in body).
    Requires is_patient manually be set to False.
    """
    data = {
        "email": "serial@test.com",
        "username": "serializer",
        "password": "pass1234",
        "password2": "pass1234",
        "is_doctor": True,
        "is_patient": False
    }
    serializer = UserRegistrationSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.email == data["email"]
    assert user.is_patient is False
    assert user.is_doctor is True

@pytest.mark.django_db
def test_user_registration_serializer_not_valid_two_differ_profiles():
    """
    Registration of an invalid profile with both is_doctor and is_patient attributes set to True.
    """
    data = {
        "email": "serial@test.com",
        "username": "serializer",
        "password": "pass1234",
        "password2": "pass1234",
        "is_doctor": True,
        "is_patient": True
    }
    serializer = UserRegistrationSerializer(data=data)
    assert serializer.is_valid() is False
    assert "two_profiles" in serializer.errors 

@pytest.mark.django_db
def test_user_registration_serializer_password_mismatch():
    data = {
        "email": "serial@test.com",
        "username": "serializer",
        "password": "pass1234",
        "password2": "wrong"
    }
    serializer = UserRegistrationSerializer(data=data)
    assert not serializer.is_valid()
    assert "password" in serializer.errors