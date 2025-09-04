from django.apps import AppConfig


class FurnitureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'furniture'

    def ready(self):
        print("🚀 signals.py loaded") 
        import furniture.signals