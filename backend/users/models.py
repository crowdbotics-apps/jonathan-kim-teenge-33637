import datetime

import stripe
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from jonathan_kim_teenge_33637 import settings

stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY if settings.STRIPE_LIVE_MODE else settings.STRIPE_SECRET_KEY

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
    stripe_customer_id = models.CharField(max_length=150, null=True, blank=True)
    is_subscribe = models.BooleanField(default=False)
    subscription_using_payment = models.BooleanField(default=False)
    subscription_using_code = models.BooleanField(default=False)

    is_premium = models.BooleanField(default=False)
    is_flaged = models.BooleanField(default=False)

# card token
#
# create card
    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        # Stripe Account Creation Of Customer
        if not self.stripe_customer_id:
            customer = stripe.Customer.create(
                description="Customer for {}".format(self.email),
                email=self.email
            )
            self.stripe_customer_id = customer.id
        super(User, self).save()

    #
    # def save(self, *args, **kwargs):
    #     self.is_staff = False if self.parent else True
    #     super().save(*args, **kwargs)
    #
    # @property
    # def is_manager(self):
    #     return self.role == User.MANAGER and self.parent
    #
    # @property
    # def is_admin(self):
    #     return self.role == User.ADMIN and not self.parent

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    name = models.CharField(_("Name"), blank=True, null=True, max_length=255)
    price = models.CharField(_("Price"), blank=True, null=True, max_length=255)
    number_of_alerts = models.CharField(_("Number of Alerts"), blank=True, null=True, max_length=255)
    is_active = models.BooleanField(default=False)