from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class Course(models.Model):

    location = models.CharField(_("Golf course Location"), blank=True, null=True, max_length=255)
    tee_datetime = models.DateField(_('Date and time'), default=timezone.now)
    no_of_selected_players = models.CharField(_("Number of selected players"), blank=True, null=True, max_length=255)
    no_of_slots_available = models.CharField(_("All slots available for selected parameters"), blank=True, null=True, max_length=255)
    no_of_max_players = models.CharField(_("Number of maximum players for opened slot"), blank=True, null=True, max_length=255)
    website_link = models.CharField(_("Website Link"), blank=True, null=True, max_length=255)
