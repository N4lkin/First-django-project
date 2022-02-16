from django.template.context_processors import static
from django.template.defaulttags import url

from .views import *
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', PizzaHome.as_view(), name='home'),
    path('promotion/', promotion, name='promotion'),
    path('support/', support, name='support'),
    path('about/', about, name='about'),
    path('faq/', faq, name='faq'),
    path('pizza/', pizza, name='pizza'),
    path('sushi/', sushi, name='sushi'),
    path('sup/', sup, name='sup'),
    path('salad/', salad, name='salad'),
    path('food/<slug:post_slug>/', show_food, name='food'),
    path('addpage/', addpage, name='addpage'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_user, name='logout'),
    path('cart/', get_cart, name='cart'),
    path('orders/', orders, name='orders'),
    path('thsfororder/', ths_for_order, name='ths_for_order')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)