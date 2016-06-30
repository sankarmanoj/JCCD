from django.shortcuts import render
from datetime import time,datetime,date
from models import dailyAttendance as attend
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
@login_required(login_url="/login/")
def attendanceHome(request):
    user = request.user
    today = attend.objects.get(employee=user,date = datetime.now().date())
    if today.inTime is not None or today.outTime is not None:
        today.present = True
        today.save()
    else:
        today.present = False
        today.save()
    days = attend.objects.filter(employee=user,date__lt=datetime.now().date())
    for day in days:
        if day.inTime is not None or day.outTime is not None:
            day.present = True
            day.save()
        else:
            day.present = False
            day.save()
    return render(request,'attend.html',{"today":today,"days":days,'currentuser':user})
