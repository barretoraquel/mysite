from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields =  '__all__'  #creates the form based on the meta data of Room in models (host, topic, etc)
