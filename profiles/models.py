from django.contrib import admin
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings

from .managers import ProfileManager


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r"^(\+\d{1,3})?,?\s?\d{8,13}",
        message="Phone number must not consist of space and requires country code. eg : +6591258565")
    phone = models.CharField(max_length=13, validators=[phone_regex], unique=True, null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    about = models.TextField(max_length=2000, blank=True)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @admin.display()
    def first_name(self):
        """
            To use first_name in list_display in admin.
            It's not possible to do something like user__first_name
        """
        return self.user.first_name

    @admin.display()
    def last_name(self):
        return self.user.last_name
