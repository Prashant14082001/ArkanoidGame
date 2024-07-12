from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
import json
import copy

def SignUpPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')

        if pass1 != pass2:
            messages.error(request, 'Passwords do not match')
        else:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'User already exists')
            else:
                try:
                    my_user = User.objects.create_user(username=uname, email=email, password=pass1)
                    my_user.save()
                    messages.success(request, 'Account created successfully')
                    return redirect('login')
                except IntegrityError:
                    messages.error(request, 'An error occurred while creating the account')

    return render(request, 'auth_System/signup.html')

def LoginPage(request):
    if request.method =='POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(request,username=username,password=pass1)
        if user:
            login(request,user)
            return redirect('arkanoid_game', room_name='room_name')
        else:
            messages.error(request, 'Invalid Credentials')
        
    return render(request,'auth_System/login.html')

@login_required(login_url='login')
def LogOutPage(request):
    logout(request)
    return redirect('login')

@login_required
def canvas(request, room_name):
    return render(request, 'canvas.html', {'room_name': room_name})

@login_required(login_url='login')
def arkanoid_game(request,room_name):
    game_params = {
        'canvas_width': 1000,
        'canvas_height': 550,
        'ball_radius': 10,
        'rect_width': 60,
        'rect_height': 20,
        'gap': 6,
        'bottom_rect_width': 100,
        'bottom_rect_height': 20,
    }
    return render(request, 'arkanoid.html', {'room_name': room_name,**game_params})



initial_game_state = {
    'ball': {
        'x': 500,
        'y': 470,
        'speed_x': 2,
        'speed_y': 2,
    },
    'paddle': {
        'x': 450,
        'y': 520,
        'width': 100,
        'height': 20,
        'speed': 60
    },
    'bricks': [
    {'x': 6 + i * 66 , 'y': 20 + j * 26 , 'status': 1}
    for j in range(8) for i in range(15)
    ],
    'lives': 2,
    'game_over': False,
    'Score': 0,
}

game_state = copy.deepcopy(initial_game_state)

def reset_game_state():
    global game_state
    game_state = copy.deepcopy(initial_game_state)

def initial_game_state_view(request):
    global game_state
    reset_game_state()
    return JsonResponse(game_state)

def reset_ball_and_paddle():
    global game_state
    game_state['ball'] = {'x': 500, 'y': 470, 'speed_x': 2, 'speed_y': 2}
    game_state['paddle'] = {'x': 450, 'y': 520, 'width': 100, 'height': 20, 'speed': 60}

def game_state_view(request):
    global game_state

    if request.method == 'POST':
        data = json.loads(request.body)
        key = data.get('key')
        if key == 'ArrowLeft':
            game_state['paddle']['x'] = max(game_state['paddle']['x'] - game_state['paddle']['speed'], 0)
        elif key == 'ArrowRight':
            game_state['paddle']['x'] = min(game_state['paddle']['x'] + game_state['paddle']['speed'], 1000 - game_state['paddle']['width'])

    ball = game_state['ball']
    ball['x'] += ball['speed_x']
    ball['y'] += ball['speed_y']

    if ball['x'] <= 0 or ball['x'] >= 1000:
        ball['speed_x'] = -ball['speed_x']
    if ball['y'] <= 0:
        ball['speed_y'] = -ball['speed_y']

    if ball['y'] >= 520 and game_state['paddle']['x'] <= ball['x'] <= game_state['paddle']['x'] + game_state['paddle']['width']:
        hit_pos = (ball['x'] - game_state['paddle']['x']) / game_state['paddle']['width']
        if hit_pos == 0.5:
            ball['speed_x'] = 2 if ball['speed_x'] > 0 else -2
            ball['speed_y'] = -2
        else:
            ball['speed_y'] *= -1

    for brick in game_state['bricks']:
        if brick['status'] == 1:
            if (brick['x'] <= ball['x'] <= brick['x'] + 60) and (brick['y'] <= ball['y'] <= brick['y'] + 20):
                if ball['speed_y'] < 0:
                    brick['status'] = 0
                    game_state['Score'] += 1
                ball['speed_y'] *= -1

    if ball['y'] >= 550:
        game_state['lives'] -= 1
        if game_state['lives'] > 0:
            reset_ball_and_paddle()
        else:
            game_state['lives'] = 0
            game_state['game_over'] = True

    return JsonResponse(game_state)
