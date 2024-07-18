from django.urls import path
from .views import *

urlpatterns = [
    path('', SignUpPage,name='signup'),
    path('logout/',LogOutPage,name = 'logout'),
    path('canvas/<str:room_name>/', canvas, name='canvas'),
    path('login/',LoginPage,name ='login'),
    path('arkanoid/<str:room_name>/', arkanoid_game, name='arkanoid_game'),
    path('game_state/', game_state_view, name='game_state'),
    path('initial_game_state/', initial_game_state_view, name='game_state'),
    
]