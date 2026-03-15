from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator


class ProjectListView(View):
    def get(self, request):
        projects = Project.objects.filter(status='open').order_by('-created_at')
        q = request.GET.get('q')
        if q:
            projects = projects.filter(Q(title__icontains=q) | Q(description__icontains=q))
        
        min_budget = request.GET.get('min_budget')
        max_budget = request.GET.get('max_budget')
        
        if min_budget:
            projects = projects.filter(budget__gte=min_budget)
        if max_budget:
            projects = projects.filter(budget__lte=max_budget)
            
        sort = request.GET.get('sort', '-created_at')
        allowed_sorts = ['budget', '-budget', 'deadline', '-deadline', '-created_at']
        if sort in allowed_sorts:
            projects = projects.order_by(sort)
        else:
            projects = projects.order_by('-created_at')
            
        paginator = Paginator(projects, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
            
        return render(request, 'projects/project_list.html', {'page_obj': page_obj})
        
    
class ProjectCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'client':
            return redirect('product_list')
        return render(request, 'projects/project_form.html')
    
    def post(self, request):
        if request.user.role != "client":
            return redirect('project_list')
        
        data = request.POST
        deadline_str = data.get('deadline')
        
        if deadline_str:
            try:
                today_str = timezone.now().strftime('%Y-%m-%d')  
                
                if deadline_str < today_str:
                    messages.error(request, "Deadline bugungi kundan oldingi sana bo'lishi mumkin emas!")
                    return render(request, 'projects/project_form.html', {'data': data})
            except Exception as e:
                messages.error(request, "Sana formatida xatolik bor.")
                return render(request, 'projects/project_form.html', {'data': data})
        Project.objects.create(
            client=request.user,
            title=data.get('title'),
            description=data.get('description'),
            budget=data.get('budget'),
            deadline=data.get('deadline')
        )
        return redirect('project_list')
    

class ProjectDetailView(View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        bids = project.bids.all()
        user_has_bid = False
        
        if request.user.is_authenticated:
            user_has_bid = bids.filter(freelancer=request.user).exists()
        
        contract = getattr(project, 'contract', None)
        context = {
            'project': project,
            'bids': bids,
            'user_has_bid': user_has_bid,
            'contract': contract,
        }
        return render(request, 'projects/project_detail.html', context)
    
    
class CancelProjectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk, client=request.user)
        
        if project.status == 'open':
            project.status = 'cancelled'
            project.save()
            messages.success(request, 'Loyiha bekor qilindi.')
        else:
            messages.error(request, 'Ish boshlangan loyihani bekor qilib bolmaydi.')
        return redirect('project_detail', pk=project.id)
    
    
class ProjectUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk, client=request.user)
        if project.status != 'open':
            messages.error(request, "Ish boshlangan loyihani tahrirlab bolmaydi.")
            return redirect('project_detail', pk=pk)
        return render(request, 'projects/project_update.html', {'project': project})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk, client=request.user)
        data = request.POST
        project.title = data.get('title')
        project.description = data.get('description')
        project.budget = data.get('budget')
        project.deadline = data.get('deadline')
        project.save()
        messages.success(request, "Loyiha muvaffaqiyatli yangilandi.")
        return redirect('project_detail', pk=pk)