from django.urls import path
from .views import DashboardView, RegisterView, VerifyView, RegisterProfileView, LoginView, LogoutView, ProfileUpdateView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyView.as_view(), name='verify_email'),
    path('register/profile/', RegisterProfileView.as_view(), name='register_profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_update'),
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]