from django.shortcuts import render,redirect
import datetime
from datetime import date
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from .models import login as log
from . import pill as pl
# Create your views here.

from django.core.files.storage import FileSystemStorage

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
def detect(request):
    msg = ""
    defect =""
    filelist= []
    if request.POST:
        f1 = request.FILES['f1']
        f2 = request.FILES['f2']
        types=request.POST["t1"]
        fs = FileSystemStorage()
        file1 = fs.save(f1.name, f1)
        print(file1)
        file2 = fs.save(f2.name, f2)
        msg = types
        if types == '1' :
            msg ="df"
            msg,defect=pl.segmentationAndComparison(file1,file2)
        elif types == "2" :
            msg = pl.roundTableForgroundBackground(file1,file2)
        elif types == "3" :
            msg = pl.singleColorPill(file1,file2)
        elif types == "4" :
            msg =pl.multiColorPill(file1,file2)
    return render(request, "det.html", {"msg": msg,"defect":defect})
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


