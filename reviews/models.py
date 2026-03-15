from django.db import models
from contracts.models import Contract
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.contract.project.title}"