from django.urls import path
from .views import BidCreateView, MyBidsListView

urlpatterns = [
    path("create/<int:project_id>/", BidCreateView.as_view(), name="bid_create"),
    path("my-bids/", MyBidsListView.as_view(), name="my_bids"),
]