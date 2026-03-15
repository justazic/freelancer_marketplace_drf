from django.urls import path
from .views import CreateReviewView

urlpatterns = [
    path("reviews/create/<int:contract_id>/", CreateReviewView.as_view()),
]