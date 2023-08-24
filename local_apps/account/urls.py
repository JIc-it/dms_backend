from django.urls import path
from .views import CheckFirstTimeLoginView, ResetPasswordView, ProfileResetPasswordView, UserListView, UserProfileView

urlpatterns = [
    path('check-first-time/', CheckFirstTimeLoginView.as_view(), name='check-first-time'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('profile-reset-password/', ProfileResetPasswordView.as_view(), name='profile-reset-password'),
    path('user-list/', UserListView.as_view(), name='user-list'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),

]
