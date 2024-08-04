# views.py
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer, BeneficiaryApplicationSerializer, LoginSerializer
from .models import MyUser, BeneficiaryApplication

class UserCreate(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        auth_login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BeneficiaryApplicationCreate(generics.CreateAPIView):
    queryset = BeneficiaryApplication.objects.all()
    serializer_class = BeneficiaryApplicationSerializer

    def perform_create(self, serializer):
        email = self.kwargs['email']
        user = MyUser.objects.get(email=email)
        serializer.save(user=user, status='pending')

class ReviewApplications(generics.ListAPIView):
    queryset = BeneficiaryApplication.objects.filter(status='pending')
    serializer_class = BeneficiaryApplicationSerializer
    permission_classes = [IsAdminUser]

class ApproveApplication(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, application_id):
        try:
            application = BeneficiaryApplication.objects.get(id=application_id)
            application.status = 'approved'
            application.save()
            return Response({'message': 'Application approved successfully'}, status=status.HTTP_200_OK)
        except BeneficiaryApplication.DoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

class RejectApplication(views.APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, application_id):
        try:
            application = BeneficiaryApplication.objects.get(id=application_id)
            application.status = 'rejected'
            application.save()
            return Response({'message': 'Application rejected successfully'}, status=status.HTTP_200_OK)
        except BeneficiaryApplication.DoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
