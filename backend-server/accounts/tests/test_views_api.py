import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser

@pytest.mark.django_db
class TestAuthEndpoints:

    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def superuser(db):
        return CustomUser.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
    
    @pytest.fixture
    def regular_user(db):
        return CustomUser.objects.create_user(
            email='reguser@example.com',
            username='regularuser',
            password='userpass567'
        )

    def test_superuser_list_all_users(self, api_client, superuser):
        """
        Superusers should get a 200 response and see the list of all users.
        """
        url = reverse('all_users')
        api_client.force_authenticate(user=superuser)

        response = api_client.get(url)

        assert response.status_code == 200

    def test_regular_user_cannot_list_all_users(self, api_client, regular_user):
        """
        Regular users should get a 403 and 'detail' message when trying to access.
        """
        url = reverse('all_users')
        api_client.force_authenticate(user=regular_user)

        response = api_client.get(url)

        assert response.status_code == 403
        assert "detail" in response.data
        assert response.data["detail"] == "You do not have permission to perform this action."

    def test_register_user(self, api_client):
        """
        User successfully registers and CustomUser model exists for that email.
        """
        url = reverse("register")  
        data = {
            "email": "newuser@test.com",
            "username": "newuser1",
            "password": "newpass123",
            "password2": "newpass123"
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == 201
        assert CustomUser.objects.filter(email="newuser@test.com").exists()

    def test_login_obtain_token(self, api_client):
        """
        User logs in and token is successfully returned in the 200 response.
        """
        user = CustomUser.objects.create_user(
            email = "login@test.com",
            username = "login1",
            password = "loginpass"
        )

        url = reverse("login")

        data = {
            "email": "login@test.com",
            "password": "loginpass"
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_token_refresh(self, api_client):
        user = CustomUser.objects.create_user(
            email = "refresh@test.com",
            username = "refresh1",
            password = "refreshpass"
        )
        
        token_url = reverse("login")

        response = api_client.post(token_url, {"email": user.email, "password": "refreshpass"}, format="json")
        refresh = response.data["refresh"]

        refresh_url = reverse("token_refresh")

        response = api_client.post(refresh_url, {"refresh": refresh}, format="json")

        assert response.status_code == 200
        assert "access" in response.data