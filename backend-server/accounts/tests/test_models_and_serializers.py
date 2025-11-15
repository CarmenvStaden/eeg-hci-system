import pytest
from accounts.models import CustomUser, DoctorProfile, PatientProfile
from accounts.serializers import UserRegistrationSerializer, AllUsersSerializer, CustomTokenObtainPairSerializer, UserRoleSerializer

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
def test_doctor_profile_creation_from_user():
    user = CustomUser.objects.create_user(
        email = "unitest@gmail.com",
        username = "uni",
        password = "abc123",
    )
    doctor = DoctorProfile.objects.create(
        user=user,
        specialization='research'
    )
    assert doctor.user.email == 'unitest@gmail.com'
    assert doctor.specialization == 'research'

@pytest.mark.django_db
def test_doctor_profile_creation_from_user():
    doctor_user = CustomUser.objects.create_user(
        email = "unitest@gmail.com",
        username = "uni",
        password = "abc123",
    )

    patient_user = CustomUser.objects.create_user(
        email = "profiletest@gmail.com",
        username = "profile",
        password = "abc123",
    )

    doctor_profile = DoctorProfile.objects.create(
        user=doctor_user,
        specialization='research'
    )

    patient_profile = PatientProfile.objects.create(
        user=patient_user,
        date_of_birth='2000-12-06',
        doctor=doctor_profile
    )

    assert patient_profile.user.email == 'profiletest@gmail.com'
    assert patient_profile.date_of_birth == '2000-12-06'
    assert doctor_profile.user.email == 'unitest@gmail.com'
    assert doctor_profile.specialization == 'research'
    assert patient_profile.doctor.user.username == 'uni'

@pytest.mark.django_db
def test_all_users_serializer():
    data = {
        "email": "serial@test.com",
        "username": "serializer",
        "password": "pass1234",
        "password2": "pass1234",
    }
    serializer = AllUsersSerializer(data=data)
    assert serializer.is_valid()

@pytest.mark.django_db
def test_user_role_serializer_valid_doctor_profile():
    """
    Registration of a profile with is_doctor set to true.
    """
    data = {
        "email": "serial@test.com",
        "username": "serializer",
        "password": "pass1234",
        "password2": "pass1234",
        "is_doctor": True,
    }
    serializer = UserRoleSerializer(data=data)
    assert serializer.is_valid()

@pytest.mark.django_db
def test_user_role_serializer_valid_patient_profile():
    """
    Registration of a profile with is_patient set to true.
    """
    data = {
        "email": "serial@test.com",
        "username": "serializer",
        "password": "pass1234",
        "password2": "pass1234",
        "is_patient": True,
    }
    serializer = UserRoleSerializer(data=data)
    assert serializer.is_valid()

@pytest.mark.django_db
def test_user_role_serializer_valid_no_profile():
    """
    Registration of a profile with is_patient set to true.
    """
    data = {
        "email": "serial@test.com",
        "username": "serializer",
        "password": "pass1234",
        "password2": "pass1234",
    }
    serializer = UserRoleSerializer(data=data)
    assert serializer.is_valid()

@pytest.mark.django_db
def test_user_role_serializer_not_valid_two_differ_profiles():
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
    serializer = UserRoleSerializer(data=data)
    assert serializer.is_valid() is False
    assert "two_profiles" in serializer.errors 

@pytest.mark.django_db
def test_user_registration_serializer_valid():
    data = {
        "email": "serial@test.com",
        "username": "serializer",
        "password": "pass1234",
        "password2": "pass1234"
    }
    serializer = UserRegistrationSerializer(data=data)
    assert serializer.is_valid()

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