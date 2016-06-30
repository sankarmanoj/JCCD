from django.shortcuts import render
from datetime import time,datetime,date,timedelta
from models import dailyAttendance as attend
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
def subtractTime(end,start):
    enddelta = timedelta(minutes = end.minute, hours = end.hour)
    startdelta = timedelta(minutes = start.minute,hours = start.hour)
    return str(enddelta - startdelta)
# Create your views here.
def AttendanceReport(request):
    users = User.objects.all()
    if request.method=="GET":
        users = User.objects.all()
        return render(request,"report.html",{"users":users})
    elif request.method=="POST":
        data = request.POST
        userpk = int(data["user"])
        user = User.objects.get(pk=userpk)
        days = attend.objects.filter(employee=user)
        return render(request,"report.html",{"days":days,"user":user,"users":users})
@login_required(login_url="/login/")
def attendanceHome(request):
    user = request.user
    if user.groups.filter(name="HRGroup").exists():
        return AttendanceReport(request)
    try:
        today = attend.objects.get(employee=user,date = datetime.now().date())
    except attend.DoesNotExist:
        today = attend.objects.create(employee=user,date = datetime.now().date())
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
def ajax(request):
    data = request.GET
    token = data["token"]
    response={}
    requestType = data["type"]
    today = attend.objects.get(modifyToken=token)
    if "in" in requestType:
        today.inTime = datetime.now().time()
        response["inTime"]=today.inTime.strftime("%I:%M %p")
    if "out" in requestType:
        today.outTime = datetime.now().time()
        response["inTime"]=today.inTime.strftime("%I:%M %p")
        response["outTime"]=today.outTime.strftime("%I:%M %p")

    today.save()
    return JsonResponse(response)
