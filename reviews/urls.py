from django.urls import path
from .views import CreateReviewView

urlpatterns = [
    path('create/<int:contract_id>/', CreateReviewView.as_view(), name='create_review'),
]