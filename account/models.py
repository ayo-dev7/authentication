from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self,email,first_name,last_name,username,password=None):
        if not email:
            raise ValueError('User must register with a valid email address.')
        if not username:
            raise ValueError('User must register with a username.')
        if not first_name:
            raise ValueError('User must register with a first name.')
        if not last_name:
            raise ValueError('User must register with a last name.')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,first_name,last_name,username,password=None):
        user = self.create_user(
            email = email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        
        user.is_admin = True
        user.is_superadmin = True
        user.is_active = True
        user.is_staff = True
        
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(max_length=100,unique=True)
    username = models.CharField(max_length=100,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    # Required
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    objects = MyAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True
