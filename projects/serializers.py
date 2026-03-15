from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField(source="client.username")
    
    class Meta:
        model = Project
        fields = "__all__"