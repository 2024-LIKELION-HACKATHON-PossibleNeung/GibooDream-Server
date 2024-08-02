from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin #추가
from django.db import models

class MyUserManager(BaseUserManager):
    # 유저(인스턴스) 생성
    def create_user(self, email, nickname, user_type, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not nickname:
            raise ValueError('The Nickname field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        if 'terms1' not in extra_fields or not extra_fields['terms1']:
            raise ValueError('Terms 1 must be accepted')
        if 'terms2' not in extra_fields or not extra_fields['terms2']:
            raise ValueError('Terms 2 must be accepted')
        if 'terms3' not in extra_fields or not extra_fields['terms3']:
            raise ValueError('Terms 3 must be accepted')
        
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    #슈퍼유저(어드민) 생성
    def create_superuser(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nickname, 'individual', password, **extra_fields)

#사용자 모델 정의 
class MyUser(AbstractBaseUser, PermissionsMixin):  #PermissionsMixin 추가
    USER_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('foreigner', 'Foreigner'),
    )

    email = models.EmailField(unique=True, primary_key=True)
    nickname = models.CharField(max_length=30, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='individual')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    terms1 = models.BooleanField(default=False)
    terms2 = models.BooleanField(default=False)
    terms3= models.BooleanField(default=False)
    terms4 = models.BooleanField(default=False, blank=True)
    terms5 = models.BooleanField(default=False, blank=True)

    donate_total = models.IntegerField(default=0, verbose_name="총 기부 금액") #추가


    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'user_type']

    def __str__(self):
        return self.email

#수혜자 신청 모델 정의
class BeneficiaryApplication(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    detailed_address = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20)
    id_number = models.CharField(max_length=20)
    proof_document = models.FileField(upload_to='proof_documents/')
    consent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return self.full_name