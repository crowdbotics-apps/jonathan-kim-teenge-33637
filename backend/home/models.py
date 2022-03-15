from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from users.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, help_text='Date Created')

    class Meta:
        abstract = True
        ordering = ('-created',)


class Wish(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    location = models.CharField(_("Location"), null=True, max_length=255)
    golfers = models.IntegerField(_("Number of Golfers"), default=0)
    from_date = models.DateTimeField(_('From Date'), default=timezone.now)
    to_date = models.DateTimeField(_('To Date'), default=False)
    is_before_selected = models.BooleanField(default=False)
    # def __str__(self):
    #     return self.title


class Course(BaseModel):
    location = models.CharField(_("Golf course Location"), blank=True, null=True, max_length=255)
    tee_datetime = models.DateTimeField(_('Date and time'), default=timezone.now)
    no_of_selected_players = models.IntegerField(_("Number of selected players"), default=0)
    no_of_slots_available = models.IntegerField(_("All slots available for selected parameters"), default=0)
    no_of_max_players = models.IntegerField(_("Number of maximum players for opened slot"), default=0)
    website_link = models.CharField(_("Website Link"), blank=True, null=True, max_length=255)


class Alert(BaseModel):
    wish = models.ForeignKey('Wish', on_delete=models.CASCADE, default=None)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    is_read = models.BooleanField(default=False)


class Setting(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    is_notifications_enabled = models.BooleanField(default=False)
    is_sms_enabled = models.BooleanField(default=False)
    is_deactivated = models.BooleanField(default=False)
