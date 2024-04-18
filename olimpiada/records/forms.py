from django import forms

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q

from .models import Record, Discipline
import datetime

User = get_user_model()



class RecordForm(forms.ModelForm):
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
        discipline = self.cleaned_data.get('discipline')
        print(discipline)
        performance_value = self.cleaned_data.get('performance')

        # Add logic to validate performance based on discipline
        # Example:
        if discipline.discipline_type == 'road':
            print(discipline.name)
            print(discipline.discipline_type)
            # validate performance as duration
            # Example: You can use Django's DurationField to validate duration
            # You may need to import datetime.timedelta for duration calculation

            # Split the time into minutes and seconds
            if ':' in performance_value:
                try:
                    minutes, seconds = performance_value.split(':')
                    # Try converting to integers
                    minutes = int(minutes)
                    seconds = float(seconds)
                except ValueError:
                    raise forms.ValidationError("Invalid time format. Please use mm:ss.ss")
            else:
                seconds = float(performance_value)
                minutes = 0

            if not (0 <= minutes < 60 and 0 <= seconds < 60):
                raise forms.ValidationError("Invalid time range.")
            # performance_value = minutes * 60 + seconds
        else:
            # Validate performance as float
            try:
                print(discipline.discipline_type)
                # Validate performance as float
                float_value = float(performance_value)
                # pass
            except ValueError:
                raise forms.ValidationError("Invalid float format")

        return performance_value

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

