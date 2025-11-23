import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from gamesession.models import Game, Prescription, EEGReading, Session
from accounts.models import CustomUser
from gamesession import views

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def doctor_user(db):
    return CustomUser.objects.create_user(
        email="doc@example.com",
        username="doc",
        password="pass",
        is_doctor=True
    )

@pytest.fixture
def patient_user(db):
    return CustomUser.objects.create_user(
        email="pat@example.com",
        username="pat",
        password="pass",
        is_patient=True
    )

@pytest.fixture
def another_patient_user(db):
    return CustomUser.objects.create_user(
        email="pat2@example.com",
        password="pass",
        is_patient=True
    )

@pytest.fixture
def game(db):
    return Game.objects.create(name="Test Game")

@pytest.fixture
def session_factory(db, game):
    def make_session(patient, **kwargs):
        return Session.objects.create(
            patient=patient,
            game=game,
            start_time=timezone.now(),
            **kwargs
        )
    return make_session

# +++ TESTS +++

@pytest.mark.django_db
def test_doctor_can_get_patient_sessions(api_client, doctor_user, patient_user, session_factory):

    session1 = session_factory(patient_user)
    session2 = session_factory(patient_user)

    api_client.force_authenticate(user=doctor_user)

    url = reverse("get_sessions_by_user_id", args=[patient_user.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert {s["id"] for s in response.data} == {session1.id, session2.id}

@pytest.mark.django_db
def test_patient_can_get_their_own_sessions(api_client, patient_user, session_factory):
    
    session1 = session_factory(patient_user)
    session2 = session_factory(patient_user)

    api_client.force_authenticate(user=patient_user)

    url = reverse("get_my_sessions")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert {s["id"] for s in response.data} == {session1.id, session2.id}