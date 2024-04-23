from django import forms

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q
import re

from .models import Record, Discipline
import datetime

User = get_user_model()



class RecordForm(forms.ModelForm):
    performance = forms.CharField(
        label='Performance',
        max_length=12,
        required=True,
        help_text="Enter performance in the format 'mm:ss.ss'"
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
            time_pattern = re.compile(r'(?P<seconds>\d{1,2}(\.\d{1,3})?)$')
            match = time_pattern.match(performance_str)

            total_seconds = float(match.group("seconds"))


        if not match:
            raise forms.ValidationError("Invalid time format. Expected 'hh:mm:ss.ss'")

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
                  'venue',
                  'record_date', ]
        widgets = {  # 'stadium': forms.RadioSelect(),
            'record_date': forms.SelectDateWidget(years=range(2003, datetime.datetime.now().year + 1)),
        }
        help_texts = {
            'performance': 'Please enter the performance in the format mm:ss.ss',
        }

