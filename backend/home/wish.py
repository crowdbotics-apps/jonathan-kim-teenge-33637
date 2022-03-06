from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Wish(models.Model):

    location = models.CharField(_("Location"), blank=True, null=True, max_length=255)
    date = models.DateField(_('Date'), default=timezone.now)
    golfers = models.CharField(_("Number of Golfers"), blank=True, null=True, max_length=255)
    from_date = models.DateField(_('From'), default=timezone.now)
    to_date = models.DateField(_('To'), default=False)
    is_before = models.BooleanField(default=False)
