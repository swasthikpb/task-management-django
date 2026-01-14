from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    ROLE_CHOICES = (
        ('SUPERADMIN', 'SuperAdmin'),
        ('ADMIN', 'Admin'),
        ('USER','User')
    )

    role = models.CharField(max_length=20, choices= ROLE_CHOICES, default='USER')
    assigned_admin = models.ForeignKey('self',on_delete = models.SET_NULL,null= True,blank= True,limit_choices_to={'role':'ADMIN'})

