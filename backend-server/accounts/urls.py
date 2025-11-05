from django.urls import path
from . import views
from accounts.views import UserRegisterCreate, UserLoginList, UserLogoutList, UserAccountsList
from rest_framework_simplejwt.views import TokenRefreshView

# URLConf
urlpatterns = [
    path('hello/', views.test_hello), # accounts/hello/
    path('users/', UserAccountsList.as_view(), name='all_users'),
    path('register/', UserRegisterCreate.as_view(), name='register'),
    path('login/', UserLoginList.as_view(), name='login'),
    path('logout/', UserLogoutList.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]