from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from .serializers import RegisterContactSerializer,UserSerializer, RegisterSerializer, LoginSerializer, LogoutSerializer
from .utils import send_otp_email, send_otp_phone_number
from rest_framework_simplejwt.tokens import RefreshToken
from bids.models import Bid
from contracts.models import Contract
from projects.models import Project
from reviews.models import Review



class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterContactSerializer
    def post(self, request):
        serializer = RegisterContactSerializer(data=request.data)
        serializer = RegisterContactSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        contact = request.data.get('contact')
        
        if not contact:
            return Response({"error": "Email yoki telefon kiriting"}, status=400)
        
        is_email = "@" in contact
        
        if is_email:
            if User.objects.filter(email=contact).exists():
                return Response({"error": "Email band"}, status=400)
            
            otp = send_otp_email(contact)
            request.session["email"] = contact
        else:
            if User.objects.filter(phone_number=contact).exists():
                return Response({"error": "Telefon band"}, status=400)
            
            otp = send_otp_phone_number(contact)
            request.session['phone_number'] = contact
        request.session["otp"] = otp
        return Response({'message':'Code yuborildi'})
    
    
class VerifyView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        code = request.data.get("code")
        session_code = request.session.get('otp')
        if code == session_code:
            return Response({"message": "Kod Tasdiqlandi"})
        return Response({"error": "Kod notogri"}, status=400)
    
    
class RegisterProfileView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": serializer.data,
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            })
        return Response(serializer.errors, status=400)
    
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response({"eror": "Login yoki parol xato"}, status=400)
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
        
        
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request):
        user = request.user
        serializer=UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(serializer.validated_data['refresh'])
            token.blacklist()
            return Response({'message':' Akkountdan muvafaqiyatli chiqdingiz'})
        
        except Exception:
            return Response({'error': "Token xato", 'status': status.HTTP_400_BAD_REQUEST})
        
        

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def get(self, request):
        if request.user.role == "client":
            my_projects = Project.objects.filter(client=request.user).order_by("-created_at")
            total_projects = my_projects.count()
            active_projects = my_projects.filter(status="in_progress").count()
            completed_projects = my_projects.filter(status="completed").count()
            total_bids = Bid.objects.filter(project__client=request.user).count()

            return Response({
                "role": "client",
                "total_projects": total_projects,
                "active_projects": active_projects,
                "completed_projects": completed_projects,
                "total_bids": total_bids
            })

        else:
            my_bids = Bid.objects.filter(freelancer=request.user)
            active_contracts = Contract.objects.filter(freelancer=request.user,status="active")
            finished_contracts = Contract.objects.filter(freelancer=request.user,status="finished")
            total_bids = my_bids.count()
            accepted_bids = my_bids.filter(status="accepted").count()

            reviews = Review.objects.filter(contract__freelancer=request.user)
            avg_rating = 0
            if reviews.exists():
                avg_rating = sum(review.rating for review in reviews) / reviews.count()
                avg_rating = round(avg_rating, 1)

            return Response({
                "role": "freelancer",
                "total_bids": total_bids,
                "accepted_bids": accepted_bids,
                "active_contracts": active_contracts.count(),
                "finished_contracts": finished_contracts.count(),
                "avg_rating": avg_rating
            })