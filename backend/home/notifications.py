from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class Notification(models.Model):

    created_at = models.DateField(_('Notification Created Date Time'), default=timezone.now)
    is_read = models.BooleanField(default=False)

    # TODO: relationshiop with course and wish