from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from users.models import User


class Wish(models.Model):

    location = models.CharField(_("Location"), null=True, max_length=255)
    golfers = models.IntegerField(_("Number of Golfers"), default=0)
    from_date = models.DateTimeField(_('From Date'), default=timezone.now)
    to_date = models.DateTimeField(_('To Date'), default=False)
    is_before_selected = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('Created at'), default=timezone.now)

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)