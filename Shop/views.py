from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404, redirect, HttpResponse, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import Product, FavoriteList, ResetPasswordToken
from .validators import *
from .forms import *
from django.core.paginator import Paginator
from django.core.mail import send_mail
from os import urandom
from binascii import hexlify
from django.utils import timezone
# Create your views here.


def main_view(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        favorite_list = FavoriteList.objects.filter(user=request.user)
        ids = [item.item.id for item in favorite_list]
    else:
        favorite_list = None
        ids = None
    best_selling_products = products.order_by('-sold_units')[:10]
    most_expensive_products = products.order_by('-price')[:10]
    newest = products.order_by('-date')[:10]
    if request.POST.get('logout') == 'True':
        logout(request)
        return redirect('main_url')
    context = {'products': products, 'newest': newest, 'add_to_cart': add_to_cart,
               'favorite_list': favorite_list, 'ids': ids, 'best_selling_products': best_selling_products,
               'most_expensive_products': most_expensive_products}
    return render(request, 'Shop/main.html', context)


def product_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.user.is_authenticated:
        favorite_list = FavoriteList.objects.filter(user=request.user)
    else:
        favorite_list = None
    return render(request, 'Shop/product.html', {'product': product, 'favorite_list': favorite_list})


def login_view(request):
    form = LoginForm
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
        try:
            user = User.objects.get(email=email)
            validate = authenticate(username=user, password=password)
            if validate is not None:
                login(request, user)
                return redirect('main_url')
        except:
            pass
    context = {'form': form,}
    return render(request, 'Shop/login.html', context)


def register_view(request):
    form = RegisterForm
    if request.POST:
        form = RegisterForm(request.POST)
        z = form
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('main_url')
    context = {'form': form,}
    return render(request, 'Shop/register.html', context)


def account_view(request, username):
    def access():
        try:
            if username == request.user.username:
                return True
            else:
                return False
        except Exception:
            return False
    change_password_form = ChangePasswordForm
    change_email_form = EmailChangeForm
    if request.user.is_authenticated:
        favorite_list = FavoriteList.objects.filter(user=request.user)
    else:
        favorite_list = None
    context = {'access': access(), 'change_password_form': change_password_form,
               'change_email_form': change_email_form, 'favorite_list': favorite_list,}
    return render(request, 'Shop/account.html', context)


def cart_view(request):
    if request.session.get('cart'):
        cart_items = request.session['cart']
        products = Product.objects.filter(pk__in=cart_items)
        items = {key: cart_items[str(key.pk)] for key in products}
        total = sum([key.price * value for key, value in items.items()])
    else:
        items = None
        total = None
    if request.user.is_authenticated:
        favorite_list = FavoriteList.objects.filter(user=request.user)
    else:
        favorite_list = None
    context = {'items': items, 'total': total, 'favorite_list': favorite_list}
    return render(request, 'Shop/cart.html', context)


def add_to_cart(request):
    primary_key = request.POST.get('add_item')
    try:
        cart_nav_validation(primary_key)
    except ValidationError:
        return HttpResponse('Incorrect ID')
    if request.session.get('cart'):
        if request.session['cart'].get(primary_key):
            request.session['cart'][primary_key] += 1
        else:
            request.session['cart'][primary_key] = 1
    else:
        request.session['cart'] = {}
        request.session['cart'][primary_key] = 1
    request.session.modified = True
    response = True
    return HttpResponse(response)


def remove_from_cart(request):
    primary_key = request.POST.get('remove_item')
    try:
        cart_nav_validation(primary_key)
    except ValidationError:
        return HttpResponse('Incorrect ID')
    if request.session.get('cart'):
        if request.session['cart'].get(primary_key):
            request.session['cart'][primary_key] -= 1
            if request.session['cart'][primary_key] < 1:
                del request.session['cart'][primary_key]
            request.session.modified = True
        else:
            return HttpResponse("Item doesn't exist in this cart")
    else:
        return HttpResponse("Cart doesn't exist")
    response = True
    return HttpResponse(response)


def delete_from_cart(request):
    primary_key = request.POST.get('delete_item')
    try:
        cart_nav_validation(primary_key)
    except ValidationError:
        return HttpResponse('Incorrect ID')
    if request.session.get('cart'):
        if request.session.get('cart').get(primary_key):
            del request.session['cart'][primary_key]
            request.session.modified = True
        else:
            return HttpResponse("Item doesn't exist in this cart")
    else:
        return HttpResponse("Cart doesn't exist")
    response = primary_key
    return HttpResponse(response)


def delete_from_favorite_list(request):
    primary_key = request.POST.get('delete_item')
    user_id = request.POST.get('user_id')
    try:
        cart_nav_validation(primary_key)
    except ValidationError:
        return HttpResponse('Incorrect ID')
    response = user_id
    FavoriteList.objects.filter(item=Product.objects.get(pk=primary_key), user=User.objects.get(pk=user_id)).delete()
    return HttpResponse(response)


def add_to_favorite_list(request):
    primary_key = request.POST.get('add_item')
    user_id = request.POST.get('user_id')
    try:
        cart_nav_validation(primary_key)
    except ValidationError:
        return HttpResponse('Błędne ID')
    response = user_id
    FavoriteList.objects.create(item=Product.objects.get(pk=primary_key), user=User.objects.get(pk=user_id))
    return HttpResponse(response)


def category_view(request, category):
    products = Product.objects.all().filter(type=category)
    if request.user.is_authenticated:
        favorite_list = FavoriteList.objects.filter(user=request.user)
        ids = [item.item.id for item in favorite_list]
    else:
        favorite_list = None
        ids = None
    p = Paginator(products, 6)
    page = request.GET.get('page')
    pages = p.get_page(page)
    context = {'products': pages,'favorite_list': favorite_list, 'ids': ids, 'p': p, 'pages': pages}
    return render(request, 'Shop/category.html', context)


def reset_password_view(request):
    form = ResetPasswordForm
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = hexlify(urandom(20)).decode()
                ResetPasswordToken(user=user, token=token, date=timezone.now()).save()
                url = reverse('reset_password_token_url', kwargs={'user': user.username, 'token': token})
                send_mail(
                    'Davi przypomnienie hasła',
                    f'Link do zmiany hasła to: {url}',
                    'daviportfoliowebsite@gmail.com',
                    [email],
                    fail_silently=False,
                    )
                return render(request, 'Shop/reset_password_check_email.html', {})
            except ObjectDoesNotExist:
                return render(request, 'Shop/reset_password_check_email_failed.html', {})
    context = {'form': form}
    return render(request, 'Shop/reset_password.html', context)


def reset_password_token_view(request, user, token):
    context = {}
    try:
        user = User.objects.get(username=user)
        validation = ResetPasswordToken.objects.get(user=user, token=token)
        if validation.is_actual():
            context['form'] = ChangePasswordForm
            return render(request, 'Shop/reset_password_token.html', context)
        else:
            return render(request, 'Shop/not_actual_reset_password_token.html', context)
    except ObjectDoesNotExist:
        return render(request, 'Shop/wrong_reset_password_token.html', context)


def change_password(request):
    if request.POST:
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            new_password2 = form.cleaned_data['new_password2']
            if new_password == new_password2:
                user = User.objects.get(username=request.user.username)
                user.set_password(new_password)
                user.save()
            response = True
    return HttpResponse(response)


def change_email(request):
    if request.POST:
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            new_email2 = form.cleaned_data['new_email2']
            if new_email == new_email2:
                user = User.objects.get(username=request.user.username)
                user.email = new_email
                user.save()
            response = True
    return HttpResponse(response)


def delete_account(request):
    try:
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        response = 'Working'
    except:
        response = 'Not working'
    return HttpResponse(response)


def search_view(request):
    if request.GET:
        search = request.GET.get('search')
        products = Product.objects.filter(title__contains=search)
        p = Paginator(products, 6)
        page = request.GET.get('page')
        pages = p.get_page(page)

    if request.user.is_authenticated:
        favorite_list = FavoriteList.objects.filter(user=request.user)
        ids = [item.item.id for item in favorite_list]
    else:
        favorite_list = None
        ids = None

    context = {'products': pages, 'favorite_list': favorite_list, 'ids': ids, 'p': p, 'search': search}
    return render(request, 'Shop/search.html', context)