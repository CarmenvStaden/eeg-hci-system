from django.urls import path
from . import views
from accounts.views import UserRegisterCreate, UserLoginList, UserLogoutList, UserAccountsList, UserRoleUpdate, DeleteUser
from rest_framework_simplejwt.views import TokenRefreshView

# URLConf
urlpatterns = [
    path('hello/', views.test_hello), # accounts/hello/
    path('users/<int:user_id>/assign-role/', UserRoleUpdate.as_view(), name='assign_user_role'), # admin only
    path('users/', UserAccountsList.as_view(), name='all_users'), # admin only
    path('register/', UserRegisterCreate.as_view(), name='register'),
    path('login/', UserLoginList.as_view(), name='login'),
    path('logout/', UserLogoutList.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('delete/user/<int:target_id>/', DeleteUser.as_view(), name='delete_user') # admin only
]