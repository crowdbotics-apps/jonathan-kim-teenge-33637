from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from home.courses import Course
from home.wish import Wish


class Notification(models.Model):

    created_at = models.DateTimeField(_('Notification Created Date Time'), default=timezone.now)
    is_read = models.BooleanField(default=False)

    wish = models.ForeignKey(Wish, on_delete=models.CASCADE, default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)