from django.apps import AppConfig


class PizzahomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pizzahome'

class CartConfig(AppConfig):
    name = 'cart'
