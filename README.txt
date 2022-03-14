Python/Django course 
This is my first Django project.
Those are my notes with the most important topics to remember when writing a project.

                    MVC - Model View Template 

------- Model--------------------------------------------------------------------------------

Each attribute of the model represents a database field.

models.py code:

from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

------- Views -------------------------------------------------------------------------------

Views act like a link between Model data and Templates 

pk stands for primary key
eg.: room/1/ --> id = pk = 1

views.py code:

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # TO UNDESTAND
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

-------Templates----------------------------------------------------------------------------

A Django template is a text document or a Python string marked-up using the Django template language. Some constructs are recognized and interpreted by the template engine. The main ones are variables and tags.
A template is rendered with a context. Rendering replaces variables with their values, which are looked up in the context, and executes tags. Everything else is output as is.

>>>>Variables:
My first name is {{ first_name }}. My last name is {{ last_name }}.

With a context of {'first_name': 'John', 'last_name': 'Doe'}, this template renders to: My first name is John. My last name is Doe.

>>>>Tags:
A tag can output content, serve as a control structure e.g. an “if” statement or a “for” loop, grab content from a database, or even enable access to other template tags
eg.: {% if user.is_authenticated %}Hello, {{ user.username }}.{% endif %} 

>>>>Filters
Filters transform the values of variables and tag arguments.



                    CRUD - Create Read Update Delete 

-------CRUD----------------------------------------------------------------------------------

eg.: "cruding" Room instances in views.py:

Create
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'polls/room_form.html', context)

Update 
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'polls/room_form.html', context)

Delete 
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'polls/delete.html', {'obj': room})

-------Database------------------------------------------------------------------------------

-------Get the project running----------------------------------------------------------------


Run migrations:  python manage.py migrate 

Make migrations: python manage.py makemigrations

Create adm user: python manage.py createsuperuser

raquelbarreto
pass12345

ghp_awPX0iDO0h8R1uMa5wvUPujYSQrmO

