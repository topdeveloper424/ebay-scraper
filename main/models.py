from django.db import models
from datetime import date

# Create your models here.

class User(models.Model):
    ADMIN_USER = 'A'
    NORMAL_USER = 'N'
    USER_ROLE_CHOICES = (
        (ADMIN_USER, 'Administrator'),
        (NORMAL_USER,'Normal User'),
    )
    
    name = models.CharField(max_length=200,null = False, default='')
    email = models.EmailField(blank=False, unique=True, default='')
    password = models.CharField(max_length=255, null = False, default='')
    avatar = models.CharField(max_length=255,null = True)
    role = models.CharField(max_length = 2, choices = USER_ROLE_CHOICES, default = NORMAL_USER)
    is_active = models.BooleanField(default=True)
    registered_at = models.DateTimeField(auto_now_add=True)

class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year_of_card = models.CharField(max_length=200,null = True)
    player_name = models.CharField(max_length=200, null=False, default='')
    set_word = models.CharField(max_length=200, null=True)
    variation = models.CharField(max_length=200, null=True)
    card = models.CharField(max_length=200, null=True)
    grade = models.CharField(max_length=200, null=True)
    terms_include = models.CharField(max_length=255, null=True)
    terms_exclude = models.CharField(max_length=255, null=True)
    
    