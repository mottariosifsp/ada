from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Course(models.Model):
    DAYS_OF_WEEK = (
        (_('Mon'), _('Monday')),
        (_('Tue'), _('Tuesday')),
        (_('Wed'), _('Wednesday')),
        (_('Thu'), _('Thursday')),
        (_('Fri'), _('Friday')),
        (_('Sat'), _('Saturday')),
        (_('Sun'), _('Sunday')),
    )

    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)

    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    def __str__(self):
        return f"{self.title}"