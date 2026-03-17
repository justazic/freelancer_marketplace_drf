from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Bid
from .serializers import BidSerializer
from projects.models import Project
from rest_framework.pagination import PageNumberPagination

class BidCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BidSerializer
    def post(self, request, project_id):
        if request.user.role != 'freelancer':
            return Response({"error": "Faqat freelancerlar bid yubora oldi", "status":status.HTTP_400_BAD_REQUEST})
        
        project = get_object_or_404(Project, id=project_id)
        
        if project.status != "open":
            return Response({"error": "Bu loyiha uchun bid yuborib bolmaydi", 'status':status.HTTP_400_BAD_REQUEST})
        
        if Bid.objects.filter(project=project, freelancer=request.user).exists():
            return Response({"error": "Siz Bu loyiha uchun allaqachon bid yuborgansiz"})
        
        serializer = BidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(freelancer=request.user, project=project)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    
class MyBidsListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BidSerializer
    def get(self, request):
        if request.user.role != 'freelancer':
            return Response({"error": 'Faqat freelancerlar', 'status':status.HTTP_403_FORBIDDEN})
        bids = Bid.objects.filter(freelancer=request.user).select_related('project')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(bids, request)
        serializer = BidSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    
        