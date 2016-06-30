from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User as djangoUser

class dailyAttendance(models.Model):
    present = models.BooleanField(default=False)
    inTime = models.TimeField(blank=True,null = True)
    outTime = models.TimeField(blank = True,null = True)
    date  = models.DateField()
    employee = models.ForeignKey(djangoUser)
    class Meta:
        unique_together = ['employee','date']
    def __unicode__(self):
        return self.employee.username + " "+str(self.date)
