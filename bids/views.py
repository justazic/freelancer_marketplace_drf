from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from projects.models import Project
from .models import Bid


class BidCreateView(LoginRequiredMixin, View):

    def post(self, request, project_id):
        if request.user.role != "freelancer":
            messages.error(request, "Faqat freelancerlar taklif yubora oladi.")
            return redirect("project_list")
        project = get_object_or_404(Project, id=project_id)

        if project.status != "open":
            messages.error(request, "Bu loyiha uchun bid yuborib bolmaydi")
            return redirect("project_detail", pk=project_id)

        if Bid.objects.filter(project=project, freelancer=request.user).exists():
            messages.error(request, "Siz bu loyiha uchun allaqachon bid yuborgansiz")
            return redirect("project_detail", pk=project_id)
        
        price = request.POST.get('price')
        message_text = request.POST.get('message')
        try:
            if not price or float(price) <= 0:
                messages.error(request, "Narx 0 dan baland bolishi kerak.")
                return redirect('project_detail', pk=project_id)
            if not message_text or len(message_text.strip()) < 10:
                messages.error(request, "Taklif xabari kamida 10 ta belgidan iborat bolishi kerak.")
                return redirect('project_detail', pk=project_id)
            Bid.objects.create(project=project,freelancer=request.user,price=price,message=message_text,)
            messages.success(request, "Sizning taklifingiz muvaffaqiyatli yuborildi!")
        except ValueError:
            messages.error(request, "Narxni raqam shaklida kiriting.")
        except Exception as e:
            messages.error(request, f"Kutilmagan xatolik yuz berdi: {e}")   
        return redirect("project_detail", pk=project_id)
    
    
    
class MyBidsListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'freelancer':
            return redirect('project_list')
        
        my_bids = Bid.objects.filter(freelancer=request.user).select_related('project')
        return render(request, 'bids/my_bids.html', {'bids': my_bids})
    