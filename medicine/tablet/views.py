from django.shortcuts import render,redirect
import datetime
from datetime import date
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from .models import login as log
# Create your views here.


def index(request):
    #log.objects.filter(username="admin",password="admin",role="user").delete()
    #log.objects.create(username="admin",password="admin",role="user")
    return render(request,"index.html",{"msg":""})

def Privacy(request):
    msg = ""
    if request.POST:
        t1 = request.POST["t1"]
        t2 = request.POST["t2"]
        id = request.session["id"]
        data = log.objects.get(logid=id)
        if data.password == t1:
            msg = "sucessfully updated"
            log.objects.filter(logid = id).update(password = t2)
        else:
            msg="invalid current password"
    return render(request,"index.html",{"msg":msg})

def Login(request):
    if request.POST:
        user = request.POST["username"]
        password = request.POST["password"]
        try:
            data = log.objects.get(username=user, password=password)
            if (data.role == "user"):
                request.session['username'] = data.username
                request.session['role'] = data.role
                request.session['id'] = data.logid
                response = redirect('/index')
                return response
            else:
                return render(request, "index.html", {"msg": "invalid account Details"})
        except:
            return render(request, "index.html", {"msg": "invalid user name or password "})
    else:
        response = redirect('/index')
        return response

def Logout(request):
    try:
        del request.session['id']
        del request.session['role']
        del request.session['username']
        response = redirect("/index?id=logout")
        return response
    except:
        response = redirect("/index?id=logout")
        return response


