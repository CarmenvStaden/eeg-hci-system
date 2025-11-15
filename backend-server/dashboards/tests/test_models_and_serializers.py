import pytest
from accounts.models import CustomUser, PatientProfile, DoctorProfile
from dashboards.serializers import PatientSerializer, DoctorSerializer, PatientAddSerializer
from rest_framework.test import APIRequestFactory

@pytest.fixture
def patient_user_data():
    return {
        "id": None, # hard-coded here, but logging
        "email": "dummypatient@gmail.com",
        "username": "dummy",
        "password": "abc123",
        "date_of_birth": None,
        "is_patient": True,
    }

@pytest.fixture
def doctor_user_data():
    return {
        "id": None, # hard-coded here, but logging
        "email": "dummydoctor@gmail.com",
        "username": "dummy",
        "password": "abc123",
        "specialization": None,
        "is_doctor": True
    }

@pytest.fixture
def patient_custom_user(db, patient_user_data):
    patient_user = CustomUser.objects.create_user(
        email = patient_user_data['email'],
        username = patient_user_data['username'],
        password = patient_user_data['password'],
        is_patient = patient_user_data['is_patient']
    )
    patient_user_data['id'] = patient_user.id
    return patient_user

@pytest.fixture
def patient_custom_user_no_tag(db, patient_user_data):
    patient_user = CustomUser.objects.create_user(
        email = patient_user_data['email'],
        username = patient_user_data['username'],
        password = patient_user_data['password']
    )
    return patient_user

@pytest.fixture
def doctor_custom_user(db, doctor_user_data):
    doctor_user = CustomUser.objects.create_user(
        email = doctor_user_data['email'],
        username = doctor_user_data['username'],
        password = doctor_user_data['password'],
        is_doctor = doctor_user_data['is_doctor']
    )
    doctor_user_data['id'] = doctor_user.id
    return doctor_user

@pytest.fixture
def doctor_custom_user_no_tag(db, doctor_user_data):
    doctor_user = CustomUser.objects.create_user(
        email = doctor_user_data['email'],
        username = doctor_user_data['username'],
        password = doctor_user_data['password']
    )
    return doctor_user

@pytest.fixture
def doctor_profile(db, doctor_custom_user):
    return doctor_custom_user.doctor_profile # .doctor_profile associates (and creates) to a DoctorProfile

@pytest.fixture
def patient_profile(db, patient_custom_user):
    return patient_custom_user.patient_profile # .patient_profile associates (and creates) to a PatientProfile

@pytest.fixture
def authenticated_request(doctor_custom_user):
    factory = APIRequestFactory()
    request = factory.post('/')
    user = doctor_custom_user
    request.user = user
    return request

@pytest.fixture
def authenticated_request_not_doc():
    factory = APIRequestFactory()
    request = factory.post('/')
    user = CustomUser.objects.create_user(
        email='notdoc@test.com',
        username='notreal',
        password='abc123'
    )
    request.user = user
    return request

# ++ Tests ++

@pytest.mark.django_db
def test_patient_profile_serializer_with_tag(patient_profile):
    """
    Tests serialization of a PatientProfile model instance into a valid JSON output.
    In cases where Admin have already assigned a role ('is_patient').    
    """
    serializer = PatientSerializer(instance=patient_profile)
    data = serializer.data
    assert data["id"] == patient_profile.id
    assert data["email"] == patient_profile.user.email
    assert data["username"] == patient_profile.user.username
    assert data["date_of_birth"] is None

@pytest.mark.django_db
def test_doctor_profile_serializer_with_tag(doctor_profile):
    """
    Tests serialization of a DoctorProfile model instance into a valid JSON output.
    In cases where Admin have already assigned a role ('is_doctor').
    """
    serializer = DoctorSerializer(instance=doctor_profile)
    data = serializer.data
    assert data["id"] == doctor_profile.id # here, id corresponds to CustomUser.DoctorProfile.id (since has tag)
    assert data["specialization"] is None

@pytest.mark.django_db
def test_doctor_profile_serializer_no_tag(doctor_profile):
    """
    Tests serialization of a DoctorProfile model instance with no 'is_doctor' tag into a valid JSON output.
    In cases where Admin have NOT assigned a role ('is_doctor'), but still valid.
    """
    serializer = DoctorSerializer(instance=doctor_profile)
    data = serializer.data
    assert data["id"] == doctor_profile.id # here, id corresponds to CustomUser.DoctorProfile.id (since has tag)
    assert data["specialization"] is None

@pytest.mark.django_db
def test_patient_add_serializer(patient_custom_user, authenticated_request):
    """
    Tests the PatientAddSerializer that takes in a patient_user_id and creates a patient-doctor relationship 
    from the patient that corresponds to the id and the logged in doctor (request.user).
    """
    patient_user_id = patient_custom_user.id

    data = {
        "patient_user_id": patient_user_id,
    }
    serializer = PatientAddSerializer(data=data, context={'request': authenticated_request})
    assert serializer.is_valid()


@pytest.mark.django_db
def test_patient_add_serializer_invalid_doctor_role(patient_custom_user, authenticated_request_not_doc):
    """
    Tests the PatientAddSerializer with an invalid doctor user (does not have is_doctor tag).
    """
    patient_user_id = patient_custom_user.id

    data = {
        "patient_user_id": patient_user_id,
    }
    serializer = PatientAddSerializer(data=data, context={'request': authenticated_request_not_doc})
    assert not serializer.is_valid()
    assert 'doctor_role_error' in serializer.errors

@pytest.mark.django_db
def test_patient_add_serializer_invalid_id(authenticated_request):
    """
    Tests PatientAddSerializer when the patient_user_id is invalid (does not exist).
    """
    patient_user_id = 10 # only one patient user total in tests

    data = {
        "patient_user_id": patient_user_id,
    }
    serializer = PatientAddSerializer(data=data, context={'request': authenticated_request})
    assert not serializer.is_valid()
    assert 'invalid_id_error' in serializer.errors

@pytest.mark.django_db
def test_patient_add_serializer_no_patient_tag(patient_custom_user_no_tag, authenticated_request):
    """
    Tests PatientAddSerializer with an invalid patient user (does not have is_patient tag).
    """
    patient_user_id = patient_custom_user_no_tag.id

    data = {
        "patient_user_id": patient_user_id,
    }
    serializer = PatientAddSerializer(data=data, context={'request': authenticated_request})
    assert not serializer.is_valid()
    assert 'patient_role_error' in serializer.errors
