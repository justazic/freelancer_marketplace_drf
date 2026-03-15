from django.urls import path
from .views import BidCreateView, MyBidsListView

urlpatterns = [
    path("bids/create/<int:project_id>/", BidCreateView.as_view()),
    path("bids/my-bids/", MyBidsListView.as_view()),
]