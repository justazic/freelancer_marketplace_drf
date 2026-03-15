from rest_framework import serializers
from .models import Contract, ChatMessage

class ContractSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField(source="client.username")
    freelancer = serializers.ReadOnlyField(source="freelancer.username")

    class Meta:
        model = Contract
        fields = "__all__"


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="sender.username")

    class Meta:
        model = ChatMessage
        fields = "__all__"