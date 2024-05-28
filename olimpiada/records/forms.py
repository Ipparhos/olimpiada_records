from django import forms
from django.utils.safestring import mark_safe

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q
import re

from .models import Record, Discipline, Athlete, Goal, Stadium
from allauth.account.forms import SignupForm
import datetime

User = get_user_model()


class StadiumForm(forms.ModelForm):
    class Meta:
        model = Stadium
        fields = ['name', 'indoors_outdoors']
        widgets = {
            'indoors_outdoors': forms.RadioSelect(choices=Stadium.INDOORS_OUTDOORS_CHOICES),
        }
        # labels= {'indoors_outdoors': "Stadium select"}

class RecordFilterForm(forms.Form):
    indoors_outdoors = forms.ChoiceField(
        choices=[('indoors', 'Indoors'), ('outdoors', 'Outdoors')],
        widget=forms.RadioSelect,
        required=False,
        # label='Stadium',
    )


class UserSignupForm(SignupForm):
    first_name = forms.CharField(max_length=120, required=True)
    last_name = forms.CharField(max_length=120, required=True)
    birth_year = forms.IntegerField(required=True)

    def save(self, request):
        user = super().save(request)

        # Set additional fields (if needed)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.birth_year = self.cleaned_data['birth_year']

        # Ensure user is saved after setting fields
        user.save()

        # Create an Athlete instance using first and last names
        Athlete.objects.create(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            birth_year=self.cleaned_data['birth_year'],
        )

        return user

class RecordForm(forms.ModelForm):
    performance = forms.CharField(
        label='Performance',
        max_length=12,
        required=True,
        help_text="Enter performance in the format 'mm:ss.ss' for road events or 'mm.cc' for field events."
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['discipline'].queryset = Discipline.objects.none()

        if 'stadium' in self.data:
            try:
                stadium_id = int(self.data.get('stadium'))
                self.fields['discipline'].queryset = Discipline.objects.filter(stadium_id=stadium_id).order_by('id')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['discipline'].queryset = self.instance.stadium.discipline_set.order_by('id')

    def clean_performance(self):
        performance_str = self.cleaned_data['performance']

        # Validate the expected format "hh:mm:ss.ss"
        try:
            time_pattern = re.compile(r'^(?P<minutes>\d{1,2}):(?P<seconds>\d{1,2}(\.\d{1,3})?)$')
            match = time_pattern.match(performance_str)
            minutes = float(match.group("minutes"))
            seconds = float(match.group("seconds"))

            total_seconds = minutes * 60 + seconds  # hours * 3600
        except:
            pass

        try:
            if not match:
                time_pattern = re.compile(r'(?P<seconds>\d{1,4}(\.\d{1,3})?)$')
                match = time_pattern.match(performance_str)

                total_seconds = float(match.group("seconds"))
        except:
            pass

        if not match:
            raise forms.ValidationError("Invalid format. Expected 'mm:ss.ss' for road events and 'mm.cc' for field evends.")

        # Convert to total seconds
        # hours = float(match.group("hours"))


        return total_seconds


    class Meta:
        model = Record
        fields = ['holder',
                  'age_group',
                  'stadium',
                  'discipline',
                  'performance',
                  'ranking',
                  'venue',
                  'wind',
                  'record_date',
                  'progression',]
        widgets = {  # 'stadium': forms.RadioSelect(),
            'record_date': forms.SelectDateWidget(years=range(2003, datetime.datetime.now().year + 1)),
        }
        help_texts = {
            'venue': "If your desired Venue doesn't appear on the list contact admin.",
            'discipline': 'Note:First select Stadium',
            'wind' : "Legal values are between -2.0 to +2.0",
            'ranking' : mark_safe("Follow this link to calculate <a href='https://caltaf.com/pointscalc/calc.html'>ranking</a>"),
            'progression' : "How many times the record has been broken."
        }

class GoalForm(forms.ModelForm):
    performance = forms.CharField(
        label='Performance',
        max_length=12,
        required=True,
        help_text="Enter performance in the format 'mm:ss.ss' for road events or 'mm.cc' for field events."
    )
    current_record = forms.CharField(
        label='Current Record(Optional)',
        max_length=12,
        required=True,
        help_text="Enter performance in the format 'mm:ss.ss' for road events or 'mm.cc' for field events."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['discipline'].queryset = Discipline.objects.none()

        if 'stadium' in self.data:
            try:
                stadium_id = int(self.data.get('stadium'))
                self.fields['discipline'].queryset = Discipline.objects.filter(stadium_id=stadium_id).order_by('id')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['discipline'].queryset = self.instance.stadium.discipline_set.order_by('id')

    def clean_performance(self):
        performance_str = self.cleaned_data['performance']
        # Validate the expected format "hh:mm:ss.ss"
        try:
            time_pattern = re.compile(r'^(?P<minutes>\d{1,2}):(?P<seconds>\d{1,2}(\.\d{1,3})?)$')
            match = time_pattern.match(performance_str)
            minutes = float(match.group("minutes"))
            seconds = float(match.group("seconds"))

            total_seconds = minutes * 60 + seconds  # hours * 3600
        except:
            pass
        try:
            if not match:
                time_pattern = re.compile(r'(?P<seconds>\d{1,4}(\.\d{1,3})?)$')
                match = time_pattern.match(performance_str)

                total_seconds = float(match.group("seconds"))
        except:
            pass

        if not match:
            raise forms.ValidationError("Invalid format. Expected 'mm:ss.ss' for road events and 'mm.cc' for field evends.")

        # Convert to total seconds
        # hours = float(match.group("hours"))
        return total_seconds

    def clean_current_record(self):
        current_record_str = self.cleaned_data['current_record']
        # Validate the expected format "hh:mm:ss.ss"
        try:
            time_pattern = re.compile(r'^(?P<minutes>\d{1,2}):(?P<seconds>\d{1,2}(\.\d{1,3})?)$')
            match = time_pattern.match(current_record_str)
            minutes = float(match.group("minutes"))
            seconds = float(match.group("seconds"))

            total_seconds = minutes * 60 + seconds  # hours * 3600
        except:
            pass

        try:
            if not match:
                time_pattern = re.compile(r'(?P<seconds>\d{1,4}(\.\d{1,3})?)$')
                match = time_pattern.match(current_record_str)

                total_seconds = float(match.group("seconds"))
        except:
            pass

        if not match:
            raise forms.ValidationError("Invalid time format. Expected 'mm:ss.ss'")

        # Convert to total seconds
        # hours = float(match.group("hours"))
        return total_seconds

    class Meta:
        model = Goal
        fields = ['athlete',
                  'age_group',
                  'stadium',
                  'discipline',
                  'current_record',
                  'performance',
                  'venue',
                  'goal_date', ]
        widgets = {  # 'stadium': forms.RadioSelect(),
            'goal_date': forms.SelectDateWidget(years=range(datetime.datetime.now().year -1, datetime.datetime.now().year + 1)),
        }
        help_texts = {
            'venue': "If your desired Venue doesn't appear on the list contact admin.",
        }