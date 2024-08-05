# urls.py
from django.urls import path
from .views import UserCreate, login, BeneficiaryApplicationCreate, ReviewApplications, ApproveApplication, RejectApplication
from donations.views import UserProfileView

urlpatterns = [
    path('signup/', UserCreate.as_view(), name='signup'),
    path('login/', login, name='login'),
    path('beneficiaries/<str:email>/', BeneficiaryApplicationCreate.as_view(), name='beneficiary_application'),
    path('applications/review/', ReviewApplications.as_view(), name='review_applications'),
    path('applications/approve/<int:application_id>/', ApproveApplication.as_view(), name='approve_application'),
    path('applications/reject/<int:application_id>/', RejectApplication.as_view(), name='reject_application'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]