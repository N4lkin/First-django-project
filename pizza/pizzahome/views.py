from datetime import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import *
from .forms import *
from .utils import *


class PizzaHome(DataMixin, ListView):
    model = Product
    template_name = 'pizzahome/catalog.html'
    success_url = reverse_lazy('food')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная Страница')
        return dict(list(context.items()) + list(c_def.items()))


def promotion(request):
    return render(request, 'pizzahome/promotion.html', {"menu": menu, "title": "Акции"})

def support(request):
    return render(request, 'pizzahome/support.html', {"menu": menu, "title": "Техническая поддержка"})

def about(request):
    return render(request, 'pizzahome/about.html', {"menu": menu, "title": "О нас"})

def faq(request):
    return render(request, 'pizzahome/faq.html', {"menu": menu, "title": "FAQ"})

def pizza(request):
    model = Product.objects.filter(type="Pizza", creation=True)
    context = {
        "menu": menu,
        "model": model,
        'title': "Пицца"
    }

    return render(request, 'pizzahome/pizza.html', context=context)

def sushi(request):
    model = Product.objects.filter(type="Sushi")
    context = {
        "menu": menu,
        "model": model,
        'title': "Суши"
    }

    return render(request, 'pizzahome/sushi.html', context=context)

def sup(request):
    model = Product.objects.filter(type="Sup")
    context = {
        "menu": menu,
        "model": model,
        'title': "Супы"
    }

    return render(request, 'pizzahome/sup.html', context=context)

def salad(request):
    model = Product.objects.filter(type="Salad")
    context = {
        "menu": menu,
        "model": model,
        'title': "Салаты"
    }

    return render(request, 'pizzahome/salad.html', context=context)

def show_food(request, post_slug):
    post = get_object_or_404(Product, slug=post_slug)
    context = {
        'post': post,
        'menu': menu,
        'title': post.name,
    }
    if request.method == 'POST':
        add_to_cart(request, post.id)
    return render(request, 'pizzahome/food.html', context=context)

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('addpage')

    else:
        form = AddPostForm()

    context = {
        'menu': menu,
        'title': 'Добавить страницу',
        'form': form,
    }
    return render(request, 'pizzahome/addpage.html', context=context)

def add_to_cart(request, food_id):
    if not Cart.objects.filter(username=request.user).exists():
        Cart.objects.create(username=request.user, creation_date=datetime.now())
    cart = Cart.objects.get(username=request.user)
    product = Product.objects.get(id=food_id)
    if request.POST.get('quantity_product') == '':
        quantity = 1
    else:
        quantity = request.POST.get('quantity_product')
    if QuantityProduct.objects.filter(username=cart, product=product).exists():
        QuantityProduct.objects.get(username=cart, product=product).delete()
        QuantityProduct.objects.create(username=cart, product=product, quantity=quantity)
    else:
        QuantityProduct.objects.create(username=cart, product=product, quantity=quantity)
    cart.product.add(Product.objects.get(id=food_id))
    cart.save()

def get_cart(request):
    if not Cart.objects.filter(username=request.user).exists():
        Cart.objects.create(username=request.user, creation_date=datetime.now())
    form = SendOrder
    cart = Cart.objects.get(username=request.user)
    product_data = cart.product.all()
    quantity_data = QuantityProduct.objects.filter(username=cart)
    user_cart = cart.product.values_list('id', flat=True)
    finally_price = get_finally_price(request)
    if request.POST.get('delete'):
        cart.product.remove(Product.objects.get(id=request.POST.get('delete')))
        quantity_delete = quantity_data.get(product=request.POST.get('delete'))
        quantity_delete.delete()
    if request.method == 'POST':
        form = SendOrder(request.POST)
        if form.is_valid():
            if Orders.objects.filter(user=cart).exists() == False:
                Orders.objects.create(**form.cleaned_data, finally_price=finally_price, user=cart)
            order = Orders.objects.get(user=cart)
            for product_id in user_cart:
                product = Product.objects.get(id=product_id)
                order.product.add(product)
                cart.product.remove(product)
                # quantity_data.get(product=product_id).delete()
            order.save()
            return redirect('ths_for_order')
    return render(request, 'pizzahome/cart.html', {'title': 'корзина', 'cart': product_data, 'quantity': quantity_data,
                                                   'menu': menu, 'form': form, 'f_price': finally_price})


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'pizzahome/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'pizzahome/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_user_context(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

def profile(request):
    return HttpResponse('Профиль')

def orders(request):
    object_orders_cart = Orders.objects.all
    quantity_data = QuantityProduct.objects.all()
    if request.POST.get('delete'):
        delete_order(request)
    if request.POST.get('in_work'):
        in_work(request)
    return render(request, 'pizzahome/order.html', {'menu': menu, 'ooc': object_orders_cart, 'q_data': quantity_data})

def delete_order(request):
    print(request.POST.get('delete'), 'ЧИАИАТАТАТА')
    Orders.objects.get(user=request.POST.get('delete')).delete()
    user_order_product = QuantityProduct.objects.filter(username=request.POST.get('delete'))
    for delete_uop in user_order_product:
        delete_uop.delete()
def in_work(request):
    order = Orders.objects.filter(user=request.POST.get('in_work'))
    order.update(in_work=True)

def ths_for_order(request):
    return render(request, 'pizzahome/ths_for_order.html', {'menu': menu})

def get_finally_price(request):
    cart = Cart.objects.get(username=request.user)
    product_data = cart.product.all()
    quantity_data = QuantityProduct.objects.filter(username=cart)
    finally_price = 0
    for product_price in product_data:
        for product_quantity in quantity_data:
            if product_price.id == product_quantity.product.id:
                finally_price += product_price.price * product_quantity.quantity
    return finally_price