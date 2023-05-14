from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from random import randint

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    
    GENDER_CHOICES = (
        ("M", "남성"),
        ("F", "여성"),
    )
    
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    # 타임존 연/월/일 
    name = models.CharField("사용자 이름",max_length=50)
    date_of_birth = models.DateField("생일",null=True)
    # age = models.IntegerField("나이",null=True, default=0)
    gender = models.CharField("성별", max_length= 5, choices=GENDER_CHOICES, default="unknown")
    # 프로필 사진 추가 upload_to = STATIC 경로 아래 저장될 폴더명
    profile_photo = models.ImageField("프로필 사진",null=True,blank=True, upload_to='img_prof')
    subscript = models.TextField("자기소개",blank=True,null=True)
    create_code = models.CharField(max_length=6,null=True,blank=True,)
    
    created = models.DateTimeField("가입 날짜",auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"    
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Follow(models.Model):
    """
    사용자 간의 팔로우/팔로워 관계를 나타내기 위한 모델.
    """
    fw = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower', verbose_name='팔로워')
    fl = models.ForeignKey(User,on_delete=models.CASCADE, related_name='follow', verbose_name='팔로우')
  
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fw','fl'], name='unique_follow')
        ]
    def clean(self):
        if self.fw == self.fl:
            raise ValidationError("자기 자신은 팔로우 할 수 없습니다.")
    
        
    def __str__(self):
        return f"{self.fw.name}님이 {self.fl.name}님을 팔로우하고 있습니다."