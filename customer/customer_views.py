import random
from datetime import date

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from account_office_engine.forms import EmployeeForm, CustomerForm, FeedbackForm, CustomerProfileForm
from account_office_engine.models import Employee, Customer, Transaction, Account, TransactionType, Feedback, Bank, \
    Notification
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
            return redirect('/c/show_transaction/')
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('/c/c_login/')
    else:
        return render(request, "c-login.html")


def customer_registration(request):
    all_banks = Bank.objects.all()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        print(f"Form Error : {form.errors}")

        contact = request.POST.get("c_contact")
        if len(contact) != 10 or not contact.isdigit():
            messages.error(request, "Contact number must be exactly 10 digits long and contain only digits.")
            return redirect('/c/c_register/')

        password = request.POST.get("c_password")
        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, e.messages)
            return redirect('/c/c_register/')

        if form.is_valid():
            try:
                form_data = form.save()
                bank_id = request.POST.get("bank_id")
                bank = Bank.objects.get(b_id=bank_id)
                Account.objects.create(c_id=form_data, b_id=bank)

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

    return render(request, 'c-register.html', {'form': form, "banks": all_banks})


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


def show_customer_transaction(request):
    if 'customer_id' in request.session:
        account = Account.objects.filter(c_id=request.session['customer_id']).first()
        all_transaction = Transaction.objects.filter(a_id=account.a_id)
        return render(request, "c-transaction.html", {'t': all_transaction})
    else:
        return render(request, "c-login.html")


def customer_money_withdraw(request):
    if 'customer_id' in request.session:
        if request.method == "POST":
            money = request.POST.get("money")
            try:
                money = float(money)
                print(f"Deposit Amount : {money}")
            except Exception as e:
                print(f"Exception Error : {e}")
                messages.error(request, "Please Enter Valid Amount !")
                return render(request, 'withdraw.html')

            account = Account.objects.filter(c_id=request.session['customer_id']).first()
            if money > 0:
                if account.a_balance >= money:
                    account.a_balance -= money
                    account.save()
                    return redirect("/c/show_account/")
                else:
                    messages.error(request, "You don't have enough balance !")
                    return render(request, 'withdraw.html')
            else:
                messages.error(request, "Please Enter Valid Amount !")
                return render(request, 'withdraw.html')
        else:
            return render(request, 'withdraw.html')
    else:
        return render(request, "c-login.html")


def customer_money_deposit(request):
    if 'customer_id' in request.session:
        if request.method == "POST":
            money = request.POST.get("money")
            try:
                money = float(money)
                print(f"Deposit Amount : {money}")
            except Exception as e:
                print(f"Exception Error : {e}")
                messages.error(request, "Please Enter Valid Amount !")
                return render(request, 'deposit.html')

            account = Account.objects.filter(c_id=request.session['customer_id']).first()
            if money > 0:
                account.a_balance += money
                account.save()
                return redirect("/c/show_account/")

            else:
                messages.error(request, "Please Enter Valid Amount !")
                return render(request, 'deposit.html')
        else:
            return render(request, 'deposit.html')
    else:
        return render(request, "c-login.html")


def transfer_money(request):
    try:
        if 'customer_id' in request.session:
            # all_accounts = Account.objects.all()
            # all_transaction_types = TransactionType.objects.all()
            banks = Bank.objects.all()
            if request.method == "POST":
                money = request.POST.get("money")
                tt_id_object = TransactionType.objects.get(tt_id=1)
                from_account_object = Account.objects.filter(c_id=request.session['customer_id']).first()
                to_account = request.POST.get("a_id")
                to_account_object = Account.objects.filter(a_id=to_account).first()

                if to_account_object is None:
                    messages.error(request, "Invalid Bank ID !")
                    return redirect("/c/money_transfer/")

                bank_name = request.POST.get("b_name")
                bank_ifsc = request.POST.get("b_ifsc")

                transfer_bank = to_account_object.b_id

                if bank_name != transfer_bank.b_name:
                    messages.error(request, "Invalid Bank !")
                    return redirect("/c/money_transfer/")

                if bank_ifsc != transfer_bank.b_ifsc:
                    messages.error(request, "Invalid IFSC Code !")
                    return redirect("/c/money_transfer/")

                try:
                    money = float(money)
                    print(f"Transfer Amount : {money}")
                except Exception as e:
                    print(f"Exception Error : {e}")
                    messages.error(request, "Please Enter Valid Amount !")
                    return redirect("/c/money_transfer/")

                if money > 0:

                    if money < from_account_object.a_balance:
                        Transaction.objects.create(
                            tt_id=tt_id_object,
                            t_amount=money,
                            a_id=from_account_object,
                            transfer_account_no=to_account_object
                        )
                        return redirect("/c/show_transaction/")
                    else:
                        messages.error(request, "Insufficient Balance !")
                        return redirect("/c/money_transfer/")
                else:
                    messages.error(request, "Please Enter Valid Amount !")
                    return redirect("/c/money_transfer/")
            else:
                return render(request, 'transfer_money.html', {"banks": banks}
                              # {"accounts": all_accounts, "transaction_types": all_transaction_types}
                              )
        else:
            return render(request, "c-login.html")

    except Exception as e:
        print(f"Exception Error : {e}")
        messages.error(request, "Something Went Wrong, Please Try Again !")
        return redirect("/c/money_transfer/")


def customer_dashboard_page(request):
    if 'customer_id' in request.session:
        today = date.today()
        customer_details = Customer.objects.get(c_id=request.session['customer_id'])
        customer_account = Account.objects.filter(c_id=customer_details).first()

        total_customers = Customer.objects.all().count()
        total_transactions = Transaction.objects.filter(a_id=customer_account).count()
        joining_date = customer_account.a_open_date
        account_balance = customer_account.a_balance
        today_transactions_details = Transaction.objects.filter(a_id=customer_account, t_date=today)

        return render(request, "c-index.html",
                      {
                          "customers": total_customers,
                          "transactions": total_transactions,
                          "joining_date": joining_date,
                          "account_balance": account_balance,
                          "today_transactions_details": today_transactions_details,
                      })
    else:
        return render(request, "c-login.html")


def show_customer_feedback(request):
    if 'customer_id' in request.session:
        feedback = Feedback.objects.filter(c_id=request.session['customer_id'])
        return render(request, "c-feedback.html", {'f': feedback})
    else:
        return render(request, "c-login.html")


def destroy_customer_feedback(request, fid):
    if 'customer_id' in request.session:
        fi = Feedback.objects.get(f_id=fid)
        fi.delete()
        return redirect("/c/show_feedback")
    else:
        return render(request, "c-login.html")


def insert_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        print(f"Form Error : {form.errors}")

        if form.is_valid():
            try:
                form.save()
                return redirect('/c/show_feedback')
            except Exception as e:
                messages.error(request, e)
                print(f'System Error : {sys.exc_info()}')
                print(f'Exception Error : {e}')
                return redirect('/c/insert_customer_feedback/')
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])
            return redirect('/c/insert_customer_feedback/')
    else:
        form = FeedbackForm()

    return render(request, 'feedback-insert.html', {'form': form})


def show_customer_profile(request):
    if 'customer_id' in request.session:
        ci = request.session['customer_id']
        cid = Customer.objects.get(c_id=ci)
        form = CustomerProfileForm(request.POST, instance=cid)
        print(f"Form Errors : {form.errors}")
        if form.is_valid():
            try:
                form.save()
                return redirect("/c/customer_profile/")
            except Exception as e:
                print(f"System Error : {sys.exc_info()}")
                print(f"Exception Error : {e}")
        return render(request, 'c-profile.html', {'cid': cid})
    else:
        return render(request, "c-login.html")


def update_customer_pass(request):
    if 'customer_id' in request.session:
        cus_id = request.session['customer_id']
        password = request.POST['pass']
        confirm_pass = request.POST['cpass']

        user = Customer.objects.get(c_id=cus_id)

        if password == confirm_pass:
            current_password = request.POST['current_password']
            val = Customer.objects.filter(c_id=cus_id, c_password=current_password)
            if val.exists():
                Customer.objects.filter(c_id=cus_id).update(c_password=confirm_pass)
                return redirect("/c/c_dashboard/")
            else:
                messages.error(request, "Something went Wrong")
                return render(request, "c-profile.html")
        else:
            messages.error(request, "New password and Confirm password does not match ")
            return render(request, 'c-profile.html', {'uid': user})
    else:
        return render(request, "c-login.html")


def all_bank(request):
    if 'customer_id' in request.session:
        banks = Bank.objects.all()
        return render(request, "c-bank.html", {'b': banks})
    else:
        return render(request, "login.html")


def notification_to_customer(request):
    if 'customer_id' in request.session:
        customers = Customer.objects.get(c_id=request.session['customer_id'])
        notification = Notification.objects.filter(c_id=customers)
        return render(request, "c-notification.html", {'n': notification})
    else:
        return render(request, "login.html")
