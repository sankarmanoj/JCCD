from __future__ import unicode_literals

from django.db import models
from datetime import time,datetime,date,timedelta
from django.contrib.auth.models import User as djangoUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
def subtractTime(end,start):
    enddelta = timedelta(minutes = end.minute, hours = end.hour)
    startdelta = timedelta(minutes = start.minute,hours = start.hour)
    return (enddelta - startdelta)
class dailyAttendance(models.Model):
    present = models.BooleanField(default=False)
    modifyToken = models.CharField(max_length=64,null = True)
    inTime = models.TimeField(blank=True,null = True)
    outTime = models.TimeField(blank = True,null = True)
    date  = models.DateField()
    employee = models.ForeignKey(djangoUser)
    def duration(self):
        difftime =  subtractTime(self.outTime ,self.inTime)
        hours = difftime.seconds/3600
        minutes = (difftime.seconds%3600)/60
        diffstring = str(hours) + " Hours " +str(minutes)+" Minutes"
        return diffstring
    class Meta:
        unique_together = ['employee','date']
    def __unicode__(self):
        return self.employee.username + " "+str(self.date)
@receiver(pre_save,sender=dailyAttendance)
def onDailySave(sender, instance, *args, **kwargs):
        if instance.inTime is not None or instance.outTime is not None:
            instance.present = True
        if instance.modifyToken is None or len(instance.modifyToken)<30:
            instance.modifyToken = get_random_string(length = 63)
            print instance.modifyToken
