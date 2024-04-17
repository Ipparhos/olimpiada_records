from django import forms
from django.contrib import admin


from .models import Athlete, Stadium, Event, AgeGroup, Place, Record

# Register your models here.

admin.site.register(Athlete)
admin.site.register(Stadium)
admin.site.register(Event)
admin.site.register(AgeGroup)
admin.site.register(Place)

admin.site.register(Record)
