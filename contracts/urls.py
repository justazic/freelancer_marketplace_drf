from django.urls import path
from .views import AcceptBidView, ContractDetailView, FinishContractView

urlpatterns = [
    path("accept-bid/<int:bid_id>/", AcceptBidView.as_view(), name="accept_bid"),
    path("finish/<int:pk>/", FinishContractView.as_view(), name="finish_contract"),
    path('contract/<int:pk>/', ContractDetailView.as_view(), name='contract_detail'),
]