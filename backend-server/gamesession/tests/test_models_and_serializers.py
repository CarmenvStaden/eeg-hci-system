import pytest
from django.utils import timezone
from unittest import mock
from gamesession.models import Game, Session, Prescription, EEGReading
from accounts.models import CustomUser
from gamesession.serializers import EEGReadingSerializer, PrescriptionSerializer, SessionSerializer, GameSerializer

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
def game_model():
    return Game.objects.create(
        name = "MindGame",
        description = None
    )

@pytest.fixture
def prescription_model(doctor_custom_user, patient_custom_user, game_model):
    mocked_datetime = timezone.datetime(2023, 1, 15, 10, 30, 0)
    
    with mock.patch('django.utils.timezone.now', return_value=mocked_datetime):

        prescription = Prescription.objects.create(
            doctor = doctor_custom_user,
            patient = patient_custom_user,
            game = game_model,
            notes = 'Play twice a week',
            created_at = mocked_datetime,
            active = True
        )
    return prescription

# +++ TESTS +++

@pytest.mark.django_db
def test_game_model_creation(game_model):
    game = game_model

    assert game.name == 'MindGame'
    assert game.description == None

@pytest.mark.django_db
def test_prescription_model_creation(prescription_model):
    prescription = prescription_model

    assert prescription.doctor.email == 'dummydoctor@gmail.com'
    assert prescription.patient.email == 'dummypatient@gmail.com'
    assert prescription.game.name == 'MindGame'
    assert prescription.notes == 'Play twice a week'
    assert prescription.active == True

    old_created_at = prescription.created_at
    assert prescription.created_at == old_created_at

@pytest.mark.django_db
def test_session_model_creation(session_model):
    session = session_model