from django.urls import path
from .views import AcceptBidView,FinishContractView,ContractDetailView

urlpatterns = [
    path("contracts/accept-bid/<int:bid_id>/", AcceptBidView.as_view()),
    path("contracts/finish/<int:pk>/", FinishContractView.as_view()),
    path("contracts/<int:pk>/", ContractDetailView.as_view()),
]