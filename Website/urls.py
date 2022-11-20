"""Website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from Shop.views import *
urlpatterns = [
    path('crud-operations/', admin.site.urls),
    path('', main_view, name='main_url'),
    path('category/<str:category>', category_view, name='category_url'),
    path('product/<int:product_id>/', product_view, name='product_url'),
    path('login/', login_view, name='login_url'),
    path('account/<str:username>', account_view, name='account_url'),
    path('register/', register_view, name='register_url'),
    path('cart/', cart_view, name='cart_url'),
    path('add-to-cart/', add_to_cart, name='add_to_cart_url'),
    path('remove-from-cart/', remove_from_cart, name='remove_from_cart_url'),
    path('delete-from-cart/', delete_from_cart, name='delete_from_cart_url'),
    path('add-to-favorite-list', add_to_favorite_list, name='add_to_favorite_list_url'),
    path('delete-from-favorite-list', delete_from_favorite_list, name='delete_from_favorite_list_url'),
    path('reset-password', reset_password_view, name='reset_password_url'),
    path('change-password', change_password, name='change_password_url'),
    path('change-email', change_email, name='change_email_url'),
    path('search', search_view, name='search_view_url'),
    path('delete_account', delete_account, name='delete_account_url'),
    path('reset-password-token/<str:user>/<str:token>', reset_password_token_view, name='reset_password_token_url'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
