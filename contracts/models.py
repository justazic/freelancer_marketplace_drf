from django.db import models
from django.conf import settings
from projects.models import Project

class Contract(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    )
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='contract')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contracts_as_client')
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contracts_as_freelancer')
    agreed_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Contract: {self.project.title}"
    
    
class ChatMessage(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']