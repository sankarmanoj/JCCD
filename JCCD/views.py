from django.shortcuts import render,redirect
from django.contrib.auth import logout,login
from django.contrib.auth import authenticate
from django.http import HttpResponse
def homepage(request):
    if request.user.is_authenticated():
        return render(request,"home.html",{"currentuser":request.user})
    else:
        return render(request,"home.html")
def logoutRequest(request):
    logout(request)
    return redirect("/")
def loginRequest(request):
    if request.method == "POST":
        data = request.POST
        try:
            nextto = data["next"]
        except:
            nextto = "/"
        user = authenticate(username = data["username"],password=data["password"])
        if user is not None:
            login(request,user)
            return redirect(nextto)
        else:
            return render(request,"login.html",{"failed":True,"next":nextto})
    elif request.GET:
        try:
            nextto = request.GET['next']
            return render(request,"login.html",{"next":nextto})
        except:
            return render(request,"login.html",{"next":"/"})
    return render(request,"login.html",{"next":"/"})
