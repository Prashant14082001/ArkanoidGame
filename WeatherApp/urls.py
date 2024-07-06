from django.urls import path
from .views import index,autocomplete

urlpatterns = [
    
    path('home/', index, name='index'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    
]