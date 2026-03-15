from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from .models import User
from bids.models import Bid
from contracts.models import Contract
from projects.models import Project
from reviews.models import Review
from django.contrib import messages
from .utils import send_otp_email, send_otp_phone_number


class RegisterView(View):
    def get(self, request):
        return render(request, "accounts/register.html")

    def post(self, request):
        contact = request.POST.get("contact")
        
        if not contact:
            return render(request, "accounts/register.html", {"error": "Email yoki telefon kiriting"})
        
        is_email = "@" in contact
        if is_email:
            if User.objects.filter(email=contact).exists():
                return render(request, 'accounts/register.html', {'error': "Bu email band"})
            otp = send_otp_email(contact)
            request.session["email"] = contact
            request.session.pop('phone_number', None)
        else:
            if User.objects.filter(phone_number=contact).exists():
                return render(request, 'accounts/register.html', {"error": "Bu telefon band"})
            otp = send_otp_phone_number(contact)
            print(f"\n----Phone Otp: {otp} ----\n")
            request.session["phone_number"] = contact
            request.session.pop("email", None)
            
        request.session["otp"] = otp
        return redirect("verify_email")
            

class VerifyView(View):
    def get(self, request):
        return render(request, "accounts/verify.html")

    def post(self, request):
        code = request.POST.get("code")
        session_code = request.session.get("otp")

        if code == session_code:
            return redirect("register_profile")
        return render(request, "accounts/verify.html", {"error": "Kod notogri"})


class RegisterProfileView(View):
    def get(self, request):
        if not request.session.get("otp"):
            return redirect("register")
        return render(request, "accounts/register_profile.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register_profile.html", {"error": "Username band"})

        email = request.session.get("email")
        phone = request.session.get("phone_number")
        user_email = email if email else None

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=user_email,
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                role=request.POST.get("role", "client"),
                bio=request.POST.get("bio")
            )

            if phone:
                user.phone_number = phone
                user.save()
            login(request, user)
            for key in ["otp", "email", "phone_number"]:
                request.session.pop(key, None)
            return redirect("project_list")
        except Exception as e:
            print(f"Baza xatosi: {e}")
            return render(request, "accounts/register_profile.html", {"error": f"Xato: {e}"})


class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("project_list")
        return render(request, "accounts/login.html", {"error": "Login yoki parol xato!"})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("login")
    
    

class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/profile_update.html")

    def post(self, request):
        user = request.user
        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.bio = request.POST.get("bio", "")
        user.email = request.POST.get('email', "")
        user.phone_number = request.POST.get('phone_number', "")
        
        if request.FILES.get("profile_picture"):
            user.profile_picture = request.FILES.get("profile_picture")
        user.save()
        messages.success(request, "Profile muvafaqiyatli yangilandi.")
        return redirect("project_list")

class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, "accounts/change_password.html", {"form": form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("project_list")
        return render(request, "accounts/change_password.html", {"form": form})
    
    
class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role == "client":
            my_projects = Project.objects.filter(client=request.user).order_by('-created_at')
            total_projects = my_projects.count()
            active_projects = my_projects.filter(status='in_progress').count()
            completed_projects = my_projects.filter(status='completed').count()
            total_bids = Bid.objects.filter(project__client=request.user).count()
            context = {
                'projects': my_projects,
                'total_projects': total_projects,
                'active_projects': active_projects,
                'completed_projects': completed_projects,
                'total_bids': total_bids,
            }
            return render(request, 'dashboard/client_dashboard.html', context)
        else:
            my_bids = Bid.objects.filter(freelancer=request.user).select_related('project').order_by('-created_at')
            active_contracts = Contract.objects.filter(freelancer=request.user, status='active').select_related('project', 'client').prefetch_related('review')
            finished_contracts = Contract.objects.filter(freelancer=request.user, status='finished').select_related('project', 'client').prefetch_related('review')
            total_bids = my_bids.count()
            accepted_bids = my_bids.filter(status='accepted').count()
            active_contracts_count = active_contracts.count()
            reviews = Review.objects.filter(contract__freelancer=request.user)
            avg_rating = 0
            if reviews.exists():
                avg_rating = sum(review.rating for review in reviews) / reviews.count()
                avg_rating = round(avg_rating, 1)
                
            context = {
                'bids': my_bids,
                'contracts': active_contracts,
                'finished_contracts': finished_contracts,
                'total_bids': total_bids,
                'accepted_bids': accepted_bids,
                'active_contracts_count': active_contracts_count,
                'avg_rating': avg_rating,
            }
            return render(request, 'dashboard/freelancer.html', context)
        