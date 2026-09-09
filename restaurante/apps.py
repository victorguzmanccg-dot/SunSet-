from django.apps import AppConfig


class RestauranteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurante'

    def ready(self):
        import restaurante.signals