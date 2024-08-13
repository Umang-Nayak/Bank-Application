"""
URL configuration for bank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from account_office_engine import views

urlpatterns = [
    # Default Page
    path("", views.dashboard_page),

    path('admin/', admin.site.urls),
    path("login/", views.admin_login),
    path("logout/", views.admin_logout),
    path("register/", views.admin_registration),
    path("dashboard/", views.dashboard_page),
    path('forgot_password/', views.forgot),
    path('send_otp/', views.sendotp),
    path('set_password/', views.set_password),

    # Customer
    path('customer/', views.show_customer),
    path('d_customer/<int:cid>', views.destroy_customer),

    # Account
    path('account/', views.show_account),
    path('d_account/<int:aid>', views.destroy_account),

    # Transaction
    path('transaction/', views.show_transaction),
    path('d_transaction/<int:tid>', views.destroy_transaction),

    # Feedback
    path('feedback/', views.show_feedback),
    path('d_feedback/<int:fid>', views.destroy_feedback),

    # Notification
    path('notification/', views.show_notification),
    path('d_notification/<int:nid>', views.destroy_notification),
    path('ni/', views.insert_notification),

    # Profile
    path('profile/', views.show_profile),
    path('update_pass/', views.update_pass),

    # Reports
    path('report1/', views.first_report),
    path('report2/', views.second_report),
    path('report3/', views.third_report),
    path('report4/', views.fourth_report),

    # Bank
    path('bank/', views.show_bank),

    path('c/', include('customer.customer_urls'))
]
