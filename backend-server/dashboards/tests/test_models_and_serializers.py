import pytest
from accounts.models import CustomUser, PatientProfile, DoctorProfile
from dashboards.serializers import PatientSerializer, DoctorSerializer, PatientAddSerializer

@pytest.fixture
def dummy_user_data():
    return {
        "id": 1, # hard-coded here, but logging
        "email": "dummyuser@gmail.com",
        "email2": "dummyDOC@test.com",
        "username": "dummy",
        "password": "abc123",
        "date_of_birth": None,
        "specialization": None,
        "is_patient": False,
        "is_doctor": False
    }

@pytest.fixture
def user(db, dummy_user_data):
    user = CustomUser.objects.create_user(
        email = dummy_user_data['email'],
        username = dummy_user_data['username'],
        password = dummy_user_data['password'],
        is_patient = dummy_user_data['is_patient'],
        is_doctor = dummy_user_data['is_doctor']
    )
    return user

@pytest.fixture
def doctor(db, dummy_user_data):
    doctor = CustomUser.objects.create_user(
        email = dummy_user_data['email2'],
        username = dummy_user_data['username'],
        password = dummy_user_data['password'],
        is_patient = dummy_user_data['is_patient'],
        is_doctor = dummy_user_data['is_doctor']
    )
    return doctor

@pytest.fixture
def doctor_profile(db, user, doctor, dummy_user_data):
    return DoctorProfile.objects.create(
        id = dummy_user_data['id'],
        user = doctor,
        specialization = dummy_user_data['specialization']
    )

@pytest.fixture
def patient_profile(db, user, doctor_profile, dummy_user_data):
    return PatientProfile.objects.create(
        id = dummy_user_data['id'],
        user = user,
        date_of_birth = dummy_user_data['date_of_birth'],
        doctor = doctor_profile
    )

@pytest.mark.django_db
def test_patient_profile_serializer(patient_profile):
    serializer = PatientSerializer(instance=patient_profile)
    data = serializer.data
    assert data["id"] == patient_profile.id
    assert data["email"] == patient_profile.user.email
    assert data["username"] == patient_profile.user.username
    assert data["date_of_birth"] is None