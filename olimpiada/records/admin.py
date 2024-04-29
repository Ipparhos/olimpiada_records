from django import forms
from django.contrib import admin


from .models import Athlete, Stadium, Discipline, AgeGroup, Venue, Record

# Register your models here.

admin.site.register(Athlete)
admin.site.register(Stadium)
admin.site.register(Discipline)
admin.site.register(AgeGroup)
admin.site.register(Venue)

admin.site.register(Record)
