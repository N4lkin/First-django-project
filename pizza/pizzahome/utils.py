menu = [
    {"title": "Главная страница", "url": "home"},
    {"title": "FAQ", "url": "faq"},
    {"title": "Акции", "url": "promotion"},
    {"title": "О нас", "url": "about"},
    {"title": "Поддержка", "url": "support"},
]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context