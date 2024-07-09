from django.urls import path
from .views import *

urlpatterns = [
    path('', SignUpPage,name='signup'),
    path('login/',LoginPage,name ='login'),
    path('logout/',LogOutPage,name = 'logout'),
    path('canvas/<str:room_name>/', canvas, name='canvas'),
    path('arkanoid/', arkanoid_game, name='arkanoid_game'),
    path('game_state/', game_state_view, name='game_state'),
    
]