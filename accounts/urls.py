from django.urls import path
from .views import RegisterUserView, UserProfileView, UserProfileImageView, VerifyUserEmail, LoginUserViews, TestAuthenticationView, PasswordResetConfirm, PasswordResetRequestView, SetNewPassword, LogoutUserView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
urlpatterns = [ 
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify'),
    path('login/', LoginUserViews.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPassword.as_view(), name='set-new-password'),
    path('logout/',LogoutUserView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('profile/image', UserProfileImageView.as_view(),name='profile-image')
    ]