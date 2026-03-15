from django.urls import path
from .views import DashboardView, LogoutView, RegisterView, VerifyView, RegisterProfileView,LoginView, ProfileUpdateView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify/", VerifyView.as_view()),
    path("register/profile/", RegisterProfileView.as_view()),
    path("login/", LoginView.as_view()),
    path("profile/", ProfileUpdateView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("dashboard/", DashboardView.as_view()),
]