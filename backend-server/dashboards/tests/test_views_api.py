import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from dashboards.views import PatientProfileList, PatientsCreateList
from accounts.models import CustomUser, DoctorProfile, PatientProfile


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def patient_1_user_data():
    return {
        "id": None, 
        "email": "patient_1@gmail.com",
        "username": "dummy_1",
        "password": "abc123",
        "date_of_birth": None,
        "is_patient": True,
    }

@pytest.fixture
def patient_2_user_data():
    return {
        "id": None, 
        "email": "patient_2@gmail.com",
        "username": "dummy_2",
        "password": "abc123",
        "date_of_birth": None,
        "is_patient": True,
    }

@pytest.fixture
def patient_3_user_data():
    return {
        "id": None, 
        "email": "patient_3@gmail.com",
        "username": "dummy_3",
        "password": "abc123",
        "date_of_birth": None,
        "is_patient": True,
    }

@pytest.fixture
def patient_1_custom_user(db, patient_1_user_data):
    patient_user = CustomUser.objects.create_user(
        email = patient_1_user_data['email'],
        username = patient_1_user_data['username'],
        password = patient_1_user_data['password'],
        is_patient = patient_1_user_data['is_patient']
    )
    patient_1_user_data['id'] = patient_user.id
    return patient_user

@pytest.fixture
def patient_2_custom_user(db, patient_2_user_data):
    patient_user = CustomUser.objects.create_user(
        email = patient_2_user_data['email'],
        username = patient_2_user_data['username'],
        password = patient_2_user_data['password'],
        is_patient = patient_2_user_data['is_patient']
    )
    patient_2_user_data['id'] = patient_user.id
    return patient_user

@pytest.fixture
def patient_3_custom_user(db, patient_3_user_data):
    patient_user = CustomUser.objects.create_user(
        email = patient_3_user_data['email'],
        username = patient_3_user_data['username'],
        password = patient_3_user_data['password'],
        is_patient = patient_3_user_data['is_patient']
    )
    patient_3_user_data['id'] = patient_user.id
    return patient_user

@pytest.fixture
def doctor_user_data():
    return {
        "id": None,
        "email": "dummydoctor@gmail.com",
        "username": "dummyDOC",
        "password": "abc123",
        "specialization": None,
        "is_doctor": True
    }

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

# +++ Tests +++ #

@pytest.mark.django_db
def test_list_all_patient_users(api_client, patient_1_custom_user, patient_2_custom_user, patient_3_custom_user, doctor_custom_user):
    """
    Tests list_all_patient_users endpoint of PatientProfileList view. 'dummyDOC' should not be returned in response.
    """
    patient_1 = patient_1_custom_user
    patient_2 = patient_2_custom_user
    patient_3 = patient_3_custom_user
    doctor_1 = doctor_custom_user

    url = reverse('list_all_patient_users')
    response = api_client.get(url)

    data = response.json()
    assert not any(item.get('username') == 'dummyDOC' for item in response.data)
    assert len(data) == 3

@pytest.mark.django_db
def test_patients_create_list_add_patients(api_client, doctor_custom_user, patient_1_custom_user):
    """
    Tests the add_patients endpoint of the PatientsCreateList view. 
    """
    url = reverse('add_patients')
    api_client.force_authenticate(user=doctor_custom_user)
    patient_user_id = patient_1_custom_user.id

    data = {
        "patient_user_id": patient_user_id
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == 201
    assert 'PatientAddSuccess' in response.data

@pytest.mark.django_db
def test_patients_create_list_list_patients(api_client, doctor_custom_user, patient_1_custom_user):
    """
    Tests the list_patients endpoint of the PatientsCreateList view. 
    """
    url = reverse('list_patients')

    doctor_profile = doctor_custom_user.doctor_profile
    patient_profile = patient_1_custom_user.patient_profile

    doctor_profile.patients.add(patient_profile)

    api_client.force_authenticate(user=doctor_custom_user)
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1  # only one patient
    assert response.data[0]["email"] == patient_1_custom_user.email

@pytest.mark.django_db
def test_patients_delete_patient(api_client, doctor_custom_user, patient_1_custom_user, patient_2_custom_user):
    """
    Tests that a doctor can remove a patient from their records.
    First adds a patient using add_patients url to the doctor record, then deletes.
    """
    add_url = reverse('add_patients')
    delete_url = reverse('delete_patient', kwargs={'patient_user_id': patient_1_custom_user.id})

    api_client.force_authenticate(user=doctor_custom_user)

    add_data = {"patient_user_id": patient_1_custom_user.id}
    add_response = api_client.post(add_url, add_data, format="json")

    assert add_response.status_code == 201
    assert len(add_response.data) == 1  # only one patient

    delete_response = api_client.delete(delete_url)

    assert delete_response.status_code == 200
    assert f"patient with user ID {patient_1_custom_user.id}" in delete_response.data
