from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import CASCADE, PROTECT, RESTRICT
from django.urls import reverse

class Product (models.Model):
    type = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media')
    content = models.TextField(blank=False)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    size = models.CharField(max_length=255)
    price = models.IntegerField()
    creation = models.BooleanField(default=True)
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Каталог"
        verbose_name_plural = "Каталог"
        ordering = ['type']


class Cart(models.Model):
    username = models.ForeignKey(User, on_delete=PROTECT)
    creation_date = models.DateTimeField(blank=True)
    product = models.ManyToManyField(Product)

    class Meta:
        verbose_name = ('Корзины')
        verbose_name_plural = ('Корзины')
        ordering = ('-creation_date',)

    def __str__(self):
        return str(self.username)

class QuantityProduct(models.Model):
    username = models.ForeignKey(Cart, on_delete=CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quantity = models.IntegerField(default=1)

class Orders(models.Model):
    user = models.ForeignKey(Cart, on_delete=CASCADE)
    city = models.CharField(max_length=255, blank=False, verbose_name='Город')
    street = models.CharField(max_length=255, blank=False, verbose_name='Улица')
    house = models.CharField(max_length=255, blank=False, verbose_name='Дом')
    apartment = models.CharField(max_length=255, blank=False, verbose_name='Квартира')
    number = models.IntegerField(blank=False, verbose_name='Телефон для связи')
    firstname = models.CharField(max_length=255, blank=False, verbose_name='Имя')
    lastname = models.CharField(max_length=255, blank=False, verbose_name='Фамилия')
    in_work = models.BooleanField(default=False, verbose_name='В работе')
    product = models.ManyToManyField(Product)
    finally_price = models.IntegerField(default=0)

    def __str__(self):
        return str(self.firstname)