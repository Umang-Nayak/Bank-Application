import random

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.dateparse import parse_date

from account_office_engine.forms import EmployeeForm, EmployeeProfileForm
from account_office_engine.models import Employee, Customer, Account, Transaction, TransactionType, Feedback, \
    Notification
import os
import sys

from bank import settings


def admin_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        val = Employee.objects.filter(e_email=email, e_password=password)
        print(f"User Email : {email} | User Password : {password}")
        if val.exists():
            val = val.first()
            request.session['employee_id'] = val.e_id
            return redirect('/customer/')
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('/login/')
    else:
        return render(request, "login.html")


def dashboard_page(request):
    if 'employee_id' in request.session:
        return render(request, "index.html")
    else:
        return render(request, "login.html")


def admin_registration(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        print(f"Form Error : {form.errors}")

        if form.is_valid():
            try:
                form.save()
                return redirect('/login')
            except Exception as e:
                messages.error(request, e)
                print(f'System Error : {sys.exc_info()}')
                print(f'Exception Error : {e}')
                return redirect('/register/')
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])
            return redirect('/register/')
    else:
        form = EmployeeForm()

    return render(request, 'register.html', {'form': form})


def admin_logout(request):
    if 'employee_id' in request.session:
        try:
            del request.session['employee_id']
        except Exception as e:
            print(f"Exception Error : {e}")
        return redirect("/login/")
    else:
        return render(request, "login.html")


def set_password(request):
    if request.method == "POST":

        T_otp = request.POST['otp']
        T_pass = request.POST['npassword']
        T_cpass = request.POST['cpassword']

        if T_pass == T_cpass:

            e = request.session['temail']
            val = Employee.objects.filter(e_email=e, otp=T_otp, otp_used=0).count()

            if val == 1:
                Employee.objects.filter(e_email=e).update(otp_used=1, e_password=T_pass)
                return redirect("/login")
            else:
                messages.error(request, "Invalid OTP")
                return render(request, "set_password.html")

        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, "set_password.html")

    else:
        return redirect("/forgot_password")


def forgot(request):
    return render(request, "forgot.html")


def sendotp(request):
    otp1 = random.randint(10000, 99999)
    e = request.POST['email']

    request.session['temail'] = e

    obj = Employee.objects.filter(e_email=e).count()

    if obj == 1:
        val = Employee.objects.filter(e_email=e).update(otp=otp1, otp_used=0)

        subject = 'Bank Management System : OTP Verification'
        message = f"Your Bank Management System OTP Verification code : {str(otp1)}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'set_password.html')

    else:
        messages.error(request, "Invalid Email")
        return render(request, "forgot.html")


def show_customer(request):
    if 'employee_id' in request.session:
        customer = Customer.objects.all()
        return render(request, "customer.html", {'c': customer})
    else:
        return render(request, "login.html")


def destroy_customer(request, cid):
    if 'employee_id' in request.session:
        ci = Customer.objects.get(c_id=cid)
        ci.delete()
        return redirect("/customer")
    else:
        return render(request, "login.html")


def show_account(request):
    if 'employee_id' in request.session:
        account = Account.objects.all()
        return render(request, "account.html", {'a': account})
    else:
        return render(request, "login.html")


def destroy_account(request, aid):
    if 'employee_id' in request.session:
        ai = Account.objects.get(a_id=aid)
        ai.delete()
        return redirect("/account")
    else:
        return render(request, "login.html")


def show_transaction(request):
    if 'employee_id' in request.session:
        transaction = Transaction.objects.all()
        return render(request, "transaction.html", {'t': transaction})
    else:
        return render(request, "login.html")


def destroy_transaction(request, tid):
    if 'employee_id' in request.session:
        ti = Transaction.objects.get(t_id=tid)
        ti.delete()
        return redirect("/transaction")
    else:
        return render(request, "login.html")


def show_feedback(request):
    if 'employee_id' in request.session:
        feedback = Feedback.objects.all()
        return render(request, "feedback.html", {'f': feedback})
    else:
        return render(request, "login.html")


def destroy_feedback(request, fid):
    if 'employee_id' in request.session:
        fi = Feedback.objects.get(f_id=fid)
        fi.delete()
        return redirect("/feedback")
    else:
        return render(request, "login.html")


def show_profile(request):
    if 'employee_id' in request.session:
        ei = request.session['employee_id']
        eid = Employee.objects.get(e_id=ei)
        form = EmployeeProfileForm(request.POST, instance=eid)
        print(f"Form Errors : {form.errors}")
        if form.is_valid():
            try:
                form.save()
                return redirect("/customer/")
            except Exception as e:
                print(f"System Error : {sys.exc_info()}")
                print(f"Exception Error : {e}")
        return render(request, 'profile.html', {'eid': eid})
    else:
        return render(request, "login.html")


def update_pass(request):
    if 'employee_id' in request.session:
        emp_id = request.session['employee_id']
        password = request.POST['pass']
        confirm_pass = request.POST['cpass']

        user = Employee.objects.get(e_id=emp_id)

        if password == confirm_pass:
            current_password = request.POST['current_password']
            val = Employee.objects.filter(e_id=emp_id, e_password=current_password)
            if val.exists():
                Employee.objects.filter(e_id=emp_id).update(e_password=confirm_pass)
                return redirect("/dashboard/")
            else:
                messages.error(request, "Something went Wrong")
                return render(request, "profile.html")
        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, 'profile.html', {'uid': user})
    else:
        return render(request, "login.html")


def first_report(request):
    if 'employee_id' in request.session:
        if request.method == "POST":
            s_d = request.POST.get('start_date')
            e_d = request.POST.get('end_date')
            start = parse_date(s_d)
            end = parse_date(e_d)
            account = Account.objects.filter(a_open_date__range=[start, end])
        else:
            account = Account.objects.all()
        return render(request, "report_1.html", {'accounts': account})
    else:
        return render(request, "login.html")


def second_report(request):
    if 'employee_id' in request.session:
        accounts = Account.objects.all()
        if request.method == "POST":
            account_id = request.POST.get('a_id')
            t = Transaction.objects.filter(a_id=account_id)

        else:
            t = Transaction.objects.all()

        return render(request, 'report_2.html', {'transaction': t, 'accounts': accounts})
    else:
        return render(request, "login.html")


def third_report(request):
    if 'employee_id' in request.session:
        transaction_type = TransactionType.objects.all()
        if request.method == "POST":
            transaction_type_id = request.POST.get('tt_id')
            t = Transaction.objects.filter(tt_id=transaction_type_id)

        else:
            t = Transaction.objects.all()

        return render(request, 'report_3.html', {'transaction': t, 'tt': transaction_type})
    else:
        return render(request, "login.html")


def fourth_report(request):
    if 'employee_id' in request.session:
        if request.method == "POST":
            s_d = request.POST.get('start_date')
            e_d = request.POST.get('end_date')
            start = parse_date(s_d)
            end = parse_date(e_d)
            transaction = Transaction.objects.filter(t_date__range=[start, end])
        else:
            transaction = Transaction.objects.all()
        return render(request, "report_4.html", {'transactions': transaction})
    else:
        return render(request, "login.html")


def show_notification(request):
    if 'employee_id' in request.session:
        notification = Notification.objects.all()
        return render(request, "notification.html", {'n': notification})
    else:
        return render(request, "login.html")


def destroy_notification(request, nid):
    if 'employee_id' in request.session:
        ni = Notification.objects.get(n_id=nid)
        ni.delete()
        return redirect("/notification")
    else:
        return render(request, "login.html")
