import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from account_office_engine.forms import EmployeeForm, CustomerForm
from account_office_engine.models import Employee, Customer, Transaction, Account
import os
import sys
from bank import settings


def customer_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        val = Customer.objects.filter(c_email=email, c_password=password)
        print(f"User Email : {email} | User Password : {password}")
        if val.exists():
            val = val.first()
            request.session['customer_id'] = val.c_id
            return redirect('/c/c_transaction/')
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('/c/c_login/')
    else:
        return render(request, "c-login.html")


def customer_dashboard_page(request):
    if 'customer_id' in request.session:
        return render(request, "c-index.html")
    else:
        return render(request, "c-login.html")


def customer_registration(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        print(f"Form Error : {form.errors}")

        if form.is_valid():
            try:
                form_data = form.save()

                Account.objects.create(c_id=form_data)
                return redirect('/c/c_login')
            except Exception as e:
                messages.error(request, e)
                print(f'System Error : {sys.exc_info()}')
                print(f'Exception Error : {e}')
                return redirect('/c/c_register/')
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])
            return redirect('/c/c_register/')
    else:
        form = CustomerForm()

    return render(request, 'c-register.html', {'form': form})


def customer_logout(request):
    if 'customer_id' in request.session:
        try:
            del request.session['customer_id']
        except Exception as e:
            print(f"Exception Error : {e}")
        return redirect("/c/c_login/")
    else:
        return render(request, "c-login.html")


def customer_set_password(request):
    if request.method == "POST":

        T_otp = request.POST['otp']
        T_pass = request.POST['npassword']
        T_cpass = request.POST['cpassword']

        if T_pass == T_cpass:

            e = request.session['temail']
            val = Customer.objects.filter(c_email=e, otp=T_otp, otp_used=0).count()

            if val == 1:
                Customer.objects.filter(c_email=e).update(otp_used=1, c_password=T_pass)
                return redirect("/c/c_login")
            else:
                messages.error(request, "Invalid OTP")
                return render(request, "c-set_password.html")

        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, "c-set_password.html")

    else:
        return redirect("/c/c_forgot_password")


def customer_forgot(request):
    return render(request, "c-forgot.html")


def customer_sendotp(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']

    request.session['temail'] = e

    obj = Customer.objects.filter(c_email=e).count()

    if obj == 1:
        val = Customer.objects.filter(c_email=e).update(otp=otp1, otp_used=0)

        subject = 'Bank Management System : OTP Verification'
        message = f"Your Bank Management System OTP Verification code : {str(otp1)}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'c-set_password.html')

    else:
        messages.error(request, "Invalid Email")
        return render(request, "c-forgot.html")


def show_customer_account(request):
    if 'customer_id' in request.session:
        accounts = Account.objects.filter(c_id=request.session['customer_id']).first()
        return render(request, "c-account.html", {'a': accounts})
    else:
        return render(request, "c-login.html")


def destroy_customer_account(request, aid):
    if 'customer_id' in request.session:
        ai = Account.objects.get(a_id=aid)
        ai.delete()
        return redirect("/c_account")
    else:
        return render(request, "c-login.html")


def customer_money_deposit(request):
    if 'customer_id' in request.session:
        if request.method == "POST":
            form = AreaForm(request.POST)
            print("-------------------", form.errors)

            if form.is_valid():
                try:
                    form.save()
                    return redirect('/area')
                except:
                    print('------------------------', sys.exc_info())

        else:
            form = Area()

        return render(request, 'Area-insert.html', {'form': form})
    else:
        return render(request, "login.html")