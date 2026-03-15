from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from contracts.models import Contract
from .models import Review


class CreateReviewView(LoginRequiredMixin, View):
    def post(self, request, contract_id):
        contract = get_object_or_404(Contract,id=contract_id,client=request.user)
        if contract.status != "finished":
            messages.error(request, "Loyiha hali tugamagan")
            return redirect("project_detail", pk=contract.project.id)

        if hasattr(contract, "review"):
            messages.error(request, "Review allaqachon yozilgan")
            return redirect("project_detail", pk=contract.project.id)
        rating = request.POST.get("rating")

        if int(rating) < 1 or int(rating) > 5:
            messages.error(request, "Rating 1 dan 5 gacha bolishi kerak")
            return redirect("project_detail", pk=contract.project.id)
        Review.objects.create(
            contract=contract,
            rating=rating,
            comment=request.POST.get("comment")
        )
        messages.success(request, "Review muvaffaqiyatli yozildi")
        return redirect("project_detail", pk=contract.project.id)