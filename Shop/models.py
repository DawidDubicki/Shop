import time

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Product(models.Model):
    product_type = [('Komputery', 'Komputery'),
                    ('Słuchawki', 'Słuchawki'),
                    ('Klawiatury', 'Klawiatury'),
                    ('Monitory', 'Monitory'),
                    ('Myszki', 'Myszki')]

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    type = models.CharField(choices=product_type, max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    sold_units = models.IntegerField(default=0)
    short_description = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=99999, decimal_places=2)
    status = models.BooleanField(default=False)

    def was_published_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)


    def __str__(self):
        return str(self.title) + ' id: ' + str(self.id)


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class FavoriteList(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item)


class UserActivity(models.Model):
    activity = [('login attempt', 'login_attempt'), ('logout', 'logout'), ('login', 'login')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_activity = models.CharField(max_length=20, choices=activity)
    date = models.DateTimeField(auto_now_add=True)


class ResetPasswordToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    token = models.CharField(max_length=40)
    date = models.DateTimeField(auto_now_add=True)

    def is_actual(self):
        if self.date >= timezone.now() - datetime.timedelta(hours=2):
            return True
        return False
