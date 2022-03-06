from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Wish(models.Model):

    location = models.CharField(_("Location"), blank=True, null=True, max_length=255)
    golfers = models.CharField(_("Number of Golfers"), blank=True, null=True, max_length=255)
    from_date = models.DateField(_('From Date'), default=timezone.now)
    to_date = models.DateField(_('To Date'), default=False)
    is_before_selected = models.BooleanField(default=False)
    created_at = models.DateField(_('Created at'), default=timezone.now)
