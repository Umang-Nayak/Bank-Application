from django.shortcuts import render, redirect
from django.contrib import messages
from account_office_engine.forms import UserForm
from account_office_engine.models import User
import os
import sys


def admin_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        val = User.objects.filter(u_email=email, u_password=password)
        print(f"User Email : {email} | User Password : {password}")
        if val.exists():
            val = val.first()
            request.session['admin_id'] = val.u_id
            return redirect('/dashboard/')
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('/login/')
    else:
        return render(request, "login.html")


def dashboard_page(request):
    if 'admin_id' in request.session:
        return render(request, "index.html")
    else:
        return render(request, "login.html")


def admin_registration(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        print(f"Form Error : {form.errors}")
        if form.is_valid():
            try:
                form.save()
                return redirect('/login')
            except Exception as e:
                print(f'System Error : {sys.exc_info()}')
                print(f'Exception Error : {e}')
    else:
        form = User()

    return render(request, 'register.html', {'form': form})


def admin_logout(request):
    if 'admin_id' in request.session:
        try:
            del request.session['admin_id']
        except Exception as e:
            print(f"Exception Error : {e}")
        return redirect("/login/")
    else:
        return render(request, "login.html")
