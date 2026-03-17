from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from contracts.models import Contract
from .models import Review
from .serializers import ReviewSerializer


class CreateReviewView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    
    def post(self, request, contract_id):
        contract = get_object_or_404(Contract,id=contract_id,client=request.user)

        if contract.status != "finished":
            return Response({"error": "Loyiha hali tugamagan"},status=status.HTTP_400_BAD_REQUEST)

        if hasattr(contract, "review"):
            return Response({"error": "Review allaqachon yozilgan"},status=status.HTTP_400_BAD_REQUEST)
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(contract=contract)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)