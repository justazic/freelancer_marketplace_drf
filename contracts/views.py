from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from bids.models import Bid
from .models import Contract, ChatMessage
from django.db import transaction
from django.contrib import messages
from django.db.models import Q


class AcceptBidView(LoginRequiredMixin, View):
    def post(self, request, bid_id):
        bid =  get_object_or_404(Bid, id=bid_id)
        project = bid.project
        
        if project.client != request.user:
            messages.error(request, "Sizda bu huquq yoq")
            return redirect("project_detail", pk=project.id)
        
        if project.status != "open":
            messages.error(request, "Bu loyiha uchun freelancer tanlangan yoki loyiha yopilgan.")
            return redirect("project_detail", pk=project.id)
        
        with transaction.atomic():
            bid.status = 'accepted'
            bid.save()
            project.bids.exclude(id=bid_id).update(status='rejected')
            project.status = 'in_progress'
            project.save()
            
            Contract.objects.create(
                project=project,
                client=project.client,
                freelancer=bid.freelancer,
                agreed_price=bid.price
            )
            
            messages.success(request, f"Muvafaqiyatli! {bid.freelancer.username} bilan shartnoma tuzildi.")
        
        return redirect('project_detail', pk=project.id)


class FinishContractView(LoginRequiredMixin, View):

    def post(self, request, pk):
        contract = get_object_or_404(
            Contract,
            pk=pk,
            client=request.user
        )
        try:
            with transaction.atomic():
                contract.status = "finished"
                contract.finished_at = timezone.now()
                contract.save()
                project = contract.project
                project.status = "completed"
                project.save()
                messages.success(request, f"Tabriklaymiz! '{project.title}' loyihasi muvaffaqiyatli yakunlandi.")
        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {e}")
        return redirect("project_detail", pk=contract.project.id)
    
    
class ContractDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        contract = get_object_or_404(Contract, Q(client=request.user) | Q(freelancer=request.user), pk=pk)
        chat_messages = contract.messages.all().order_by('created_at')
        review = getattr(contract, 'review', None)
        context = {
            'contract': contract,
            'chat_messages': chat_messages,
            'review': review
        }
        return render(request, 'contracts/contract_detail.html', context)

    def post(self, request, pk):
        contract = get_object_or_404(Contract, Q(client=request.user) | Q(freelancer=request.user), pk=pk)
        text = request.POST.get('message_text')
        if contract.status == "finished":
            messages.info(request, "Shartnoma yakunlangan, xabar yuborib bolmaydi.")
            return redirect('contract_detail', pk=pk)
        text = request.POST.get('message_text', '').strip()
        if text:
            ChatMessage.objects.create(contract=contract,sender=request.user,text=text)
        else:
            messages.error(request, "Xabar matni bo'sh bolishi mumkin emas.")  
        return redirect('contract_detail', pk=pk)