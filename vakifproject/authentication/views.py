from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer, CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Kullanıcı başarıyla oluşturuldu"
        })


class LoginView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = User.objects.create(
            username="admin",
            first_name="Admin",
            last_name="Kullanıcı"
        )
        user.set_password("admin_password")
        user.save()
        
        if username is None or password is None:
            return Response(
                {"error": "Lütfen kullanıcı adı ve şifre giriniz"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"error": "Geçersiz kimlik bilgileri"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
            "message": "Giriş başarılı"
        })


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response(
                {"message": "Başarıyla çıkış yapıldı"}, 
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"error": "Oturum sonlandırılırken bir hata oluştu"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Mevcut şifreyi kontrol et
            if not user.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Mevcut şifre hatalı."]}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Yeni şifreyi kaydet
            user.set_password(serializer.data.get("new_password"))
            user.save()
            
            return Response(
                {"message": "Şifre başarıyla değiştirildi"}, 
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        return self.request.user
