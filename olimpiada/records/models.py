from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from django.utils import timezone
from django.conf import settings

User = settings.AUTH_USER_MODEL
# USERNAME_REGEX = '^[a-zA-Z0-9_@.+-]'

road_disciplines = ['60m', '60m Hurdles', '100m', '100m Hurdles', '110m Hurdles', '200m', '400m', '400m Hurdles', '800m',
                    '1500m', '3000m', '3000m Steeplechase', '5000m', '10000m']
field_disciplines = ['Long Jump', 'Triple Jump', 'High Jump', 'Pole Vault', 'Javelin Throw', 'Shot Put',
                     'Hammer Throw', 'Discus Throw']


class Athlete(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    birth_year = models.IntegerField(default=None, blank=True, null=True)

    @property
    def full_name(self):
        """Returns the person's full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name_with_birthyear(self):
        """Returns the person's full name and the last 2 digits of birth year."""
        return f"{self.full_name} ({str(self.birth_year)[2:]})"

    def __str__(self):
        return self.full_name


class Stadium(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Discipline(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)

    @property
    def discipline_type(self):
        if self.name in road_disciplines:
            return 'road'
        else:
            return 'field'

    class Meta:
        unique_together = [('stadium', 'name')]

    def __str__(self):
        return f"{self.name} {self.stadium}"


class AgeGroup(models.Model):
    age_group = models.CharField(max_length=10)

    def __str__(self):
        return self.age_group


class Place(models.Model):
    area = models.CharField(max_length=30)
    stadium_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.stadium_name}, {self.area}"


class Record(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    holder = models.ForeignKey(Athlete, blank=True, null=True, on_delete=models.SET_NULL)
    # description = models.TextField()
    age_group = models.ForeignKey(AgeGroup, blank=True, null=True, on_delete=models.SET_NULL)
    discipline = models.ForeignKey(Discipline, blank=True, null=True, on_delete=models.SET_NULL)
    place = models.ForeignKey(Place, blank=True, null=True, on_delete=models.SET_NULL)
    stadium = models.ForeignKey(Stadium, blank=True, null=True, on_delete=models.SET_NULL)
    performance = models.CharField(max_length=10, blank=False, null=True)
    # performance2 = models.DurationField(blank=True, null=True)
    record_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.holder.__str__()

    def get_absolute_url(self):
        return f'/records/{self.pk}/'

    def get_edit_url(self):
        return f'/records/'

    def get_delete_url(self):
        return f'/records/{self.pk}/delete/'

    class Meta:
        ordering = ['performance', '-record_date']
        # verbose_name = ''  # How admin sees the name for single obj
        # verbose_name_plural = 'Records' # How admin sees the name for multiple objs
        unique_together = [['holder', 'discipline', 'performance']]
        db_table = 'Olimpiada records'
