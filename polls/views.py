from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import UserCreationForm 
from .models import Room, Topic
from .forms import RoomForm


# rooms = [
    #{'id': 1, 'name': 'Lets learn python!'},
    #{'id': 2, 'name': 'Design with me'},
    #{'id': 3, 'name': 'Frontend developers'},
#]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()   #get user's username and password   
        password = request.POST.get('password')

        try:    
            user = User.objects.get(username=username) #check if user exists cheking username 
        except:
            messages.error(request, 'User does not exist') #if username dont exist returns a message 

        user = authenticate(request, username=username, password=password) # make sure the credentials are correct wwith the correct password

        if user is not None:          
            login(request, user)        #logs the user in and returns to home 
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page': page}
    return render(request, 'polls/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    else:
        messages.error(request, 'An error ocurred during registration')
    return render(request, 'polls/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # TO UNDERSTAND
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        # Q(host__name__icontains=q) what if I want to filter by host
    )  # query list of rooms 
    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'polls/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)     # query room is the instance of Room where the id = pk
    context = {'room': room}
    return render(request, 'polls/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'polls/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Youre are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'polls/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'polls/delete.html', {'obj': room})
    