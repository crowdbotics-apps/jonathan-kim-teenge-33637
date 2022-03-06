import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

MALE = 'male'
FEMALE = 'female'
UNDEFINED = 'undefined'
GENDER_OPTIONS = [
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (UNDEFINED, 'Undefined')
]

class User(AbstractUser):
    # WARNING!
    """
    Some officially supported features of Crowdbotics Dashboard depend on the initial
    state of this User model (Such as the creation of superusers using the CLI
    or password reset in the dashboard). Changing, extending, or modifying this model
    may lead to unexpected bugs and or behaviors in the automated flows provided
    by Crowdbotics. Change it at your own risk.


    This model represents the User instance of the system, login system and
    everything that relates with an `User` is represented by this model.
    """

    # First Name and Last Name do not cover name patterns
    # around the globe.

    name = models.CharField(_("Full Name"), blank=True, null=True, max_length=255)
    email = models.CharField(_("Email"), blank=True, null=True, max_length=255)
    phone_number = models.CharField(_("Phone number"), blank=True, null=True, max_length=255)
    dob = models.DateField(_('Date of birth'), default=timezone.now)
    gender = models.CharField(_("Gender"), blank=True, null=True, max_length=255, choices=GENDER_OPTIONS)
    address = models.CharField(_("Address"), blank=True, null=True, max_length=255)
    city = models.CharField(_("City"), blank=True, null=True, max_length=255)
    zip_code = models.CharField(_("Zip Code"), max_length=150, null=True, blank=True)
    state = models.CharField(_("State"), blank=True, null=True, max_length=255)
    country = models.CharField(_("Country"), blank=True, null=True, max_length=255)
    profile_picture = models.ImageField(upload_to='user_profile_pictures', blank=True, null=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
