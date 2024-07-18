from django.apps import AppConfig


# class WeatherappConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "WeatherApp"


from django.apps import AppConfig


class WeatherAppConfig(AppConfig):
    name = 'WeatherApp'

    def ready(self):
        import WeatherApp.signals  
