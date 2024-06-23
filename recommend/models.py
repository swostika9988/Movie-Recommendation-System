from django.db import models

# Create your models here.

class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

# create table for user

class User(DateTimeModel):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,null=True)

    


