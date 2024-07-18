from django.urls import path
from .views import index,autocomplete
from . import views

urlpatterns = [
    
    path('home/', index, name='index'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    path('upload/', views.upload_image, name='upload_image'),
    path('images/', views.image_list, name='image_list'),
    
]