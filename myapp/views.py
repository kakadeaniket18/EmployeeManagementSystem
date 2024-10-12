from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Employee
from .forms import EmployeeInfoForm
from django.db.models import Q
from django.views import View

class employee_details(View):
    def get(self, request):
        employee=Employee.objects.all().values()
        return render(request,'employee_details.html',{"employee":employee})

class employee_update(View):
    def get(self,request,id):
        if request.method=="POST":
            employee=Employee.objects.get(pk=id)
            fm=EmployeeInfoForm(request.POST,instance=employee)
            if fm.is_valid:
                fm.save()
                return HttpResponseRedirect("/home")
        else:
            employee=Employee.objects.get(pk=id)
            fm=EmployeeInfoForm(instance=employee)
        return render(request,"employee_update.html",{"form":fm})

class employee_delete(View):
    def get(self,request,id):
        if request.method=="POST":
            employee=Employee.objects.get(pk=id)
            employee.delete()
            return HttpResponseRedirect("/home")

class employee_add(View):
    def get(self,request):
        if request.method=="POST":
            fm=EmployeeInfoForm(request.POST)
            if fm.is_valid:
                fm.save()
                return HttpResponseRedirect("/home")
        else:
            fm=EmployeeInfoForm()
        return render(request,"employee_add.html",{"form":fm})

class employee_search(View):
    def get(self,request):
        if request.method=="POST":
            search=request.POST.get("output")
            employee=Employee.objects.all()
            sta=None
            if search:
                sta=employee.filter(
                    Q(fname__icontains=search)|
                    Q(lname__icontains=search)|
                    Q(age__icontains=search)|
                    Q(address__icontains=search))
            return render(request,"employee_details.html",{"employee":sta})
        else:
            return HttpResponse("An error occured")