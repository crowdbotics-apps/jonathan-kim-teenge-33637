from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class Notification(models.Model):

    location = models.CharField(_("Location"), blank=True, null=True, max_length=255)
    created_at = models.DateField(_('Notification Created Date Time'), default=timezone.now)
    is_read = models.BooleanField(default=False)
    tee_time = models.DateField(_('Time and Date'), default=timezone.now)
    no_of_selected_golfers = models.CharField(_("Number of selected players"), blank=True, null=True, max_length=255)
    no_of_slots_available = models.CharField(_("Number of slots available"), blank=True, null=True, max_length=255)
    no_of_max_players = models.CharField(_("Number of maximum players for opened slot"), blank=True, null=True, max_length=255)
