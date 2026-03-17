from rest_framework import serializers
from .models import Bid

class BidSerializer(serializers.ModelSerializer):
    freelancer = serializers.ReadOnlyField(source='freelancer.username')
    
    class Meta:
        model = Bid
        fields = "__all__"
        read_only_fields = ('project', 'freelancer')