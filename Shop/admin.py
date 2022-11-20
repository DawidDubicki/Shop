from django.contrib import admin
from .models import Product, FavoriteList
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'quantity', 'status']
    search_fields = ['id', 'title']
    list_filter = ['status']


@admin.register(FavoriteList)
class FavoriteListAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', 'user']
