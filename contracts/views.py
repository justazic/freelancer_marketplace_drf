from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from bids.models import Bid
from projects.models import Project
from .models import Contract, ChatMessage
from .serializers import ContractSerializer, ChatMessageSerializer


class AcceptBidView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContractSerializer
    def post(self, request, bid_id):
        bid = get_object_or_404(Bid, id=bid_id)
        project = bid.project
        if project.client != request.user:
            return Response({'error': "Sizda bu huquq yoq", 'status':status.HTTP_403_FORBIDDEN})
        
        if project.status != "open":
            return Response({'error': 'Freelancer allaqachon tanlangan', 'status':status.HTTP_400_BAD_REQUEST})
        
        with transaction.atomic():
            bid.status = "accepted"
            bid.save()
            project.bids.exclude(id=bid_id).update(status="rejected")
            project.status = "in_progress"
            project.save()
            contract = Contract.objects.create(
                project=project,
                client=project.client,
                freelancer=bid.freelancer,
                agreed_price=bid.price
            )
        serializer = ContractSerializer(contract)
        return Response(serializer.data, status=201)
    
    
class FinishContractView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContractSerializer
    def post(self, request, pk):
        contract = get_object_or_404(Contract,pk=pk,client=request.user)
        with transaction.atomic():
            contract.status = "finished"
            contract.finished_at = timezone.now()
            contract.save()
            project = contract.project
            project.status = "completed"
            project.save()
        return Response({"message": "Loyiha muvaffaqiyatli yakunlandi"})
    
    
class ContractDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer
    def get(self, request, pk):
        contract = get_object_or_404(Contract,Q(client=request.user) | Q(freelancer=request.user),pk=pk)
        messages = contract.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        if serializer.is_valid():
            serializer.save(contract=contract, sender=request.user)
    
        contract_serializer = ContractSerializer(contract)
        return Response({"contract": contract_serializer.data,"messages": serializer.data})

    def post(self, request, pk):
        contract = get_object_or_404(Contract,Q(client=request.user) | Q(freelancer=request.user),pk=pk)
        if contract.status == "finished":
            return Response({"error": "Shartnoma yakunlangan"},status=status.HTTP_400_BAD_REQUEST)
        text = request.data.get("text")
        if not text:
            return Response({"error": "Xabar bo'sh"},status=status.HTTP_400_BAD_REQUEST)
        message = ChatMessage.objects.create(contract=contract,sender=request.user,text=text)
        serializer = ChatMessageSerializer(message)
        return Response(serializer.data, status.HTTP_201_CREATED)