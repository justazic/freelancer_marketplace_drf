from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.pagination import PageNumberPagination


class ProjectListView(APIView):

    def get(self, request):
        projects = Project.objects.filter(status='open')
        q = request.query_params.get('q')
        if q:
            projects = projects.filter(Q(title__icontains=q) |Q(description__icontains=q))
        min_budget = request.query_params.get('min_budget')
        max_budget = request.query_params.get('max_budget')

        if min_budget:
            projects = projects.filter(budget__gte=min_budget)

        if max_budget:
            projects = projects.filter(budget__lte=max_budget)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(projects, request)
        serializer = ProjectSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    

class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if request.user.role != 'client':
            return Response({"error": "Faqat client loyiha yaratishi mumkin", 'status': status.HTTP_403_FORBIDDEN})
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    
class ProjectDetailView(APIView):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serrializer = ProjectSerializer(project)
        return Response(serrializer.data)
    
    
class ProjectUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, request, pk):
        project = get_object_or_404(Project, pk=pk, client=request.user)
        if project.status != 'open':
            return None
        return project
    
    def patch(self, request, pk):
        project = self.get_object(request, pk)
        
        if not project:
            return Response({'error': "Ish boshlangan loyihani tahrirlab bomaydi", 'status': status.HTTP_400_BAD_REQUEST})
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        project = self.get_object(request, pk)
        if not project:
            return Response({'error':'Ish boshlangan loyihani tahrirlab bolmaydi', 'status':status.HTTP_400_BAD_REQUEST})
        serializer=ProjectSerializer(project, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CancelProjectView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk, client=request.user)
        
        if project.status != "open":
            return Response({"error":"Ish boshlangan loyihani bekor qilib bolmaydi", "status":status.HTTP_400_BAD_REQUEST})
        project.status = 'cancelled'
        project.save()
        return Response({"message": "Loyiha bekor qilindi"})
    