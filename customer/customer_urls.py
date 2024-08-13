from django.urls import path
from customer import customer_views

urlpatterns = [

    path("c_login/", customer_views.customer_login),
    path("c_logout/", customer_views.customer_logout),
    path("c_register/", customer_views.customer_registration),
    path("c_dashboard/", customer_views.customer_dashboard_page),
    path('c_forgot_password/', customer_views.customer_forgot),
    path('c_send_otp/', customer_views.customer_sendotp),
    path('c_set_password/', customer_views.customer_set_password),


    # Account
    path('show_account/', customer_views.show_customer_account),
    path('delete_account/', customer_views.destroy_customer_account),

    # Feedback
    path('show_feedback/', customer_views.show_customer_feedback),
    path('delete_feedback/', customer_views.destroy_customer_feedback),
    path('insert_customer_feedback/', customer_views.insert_feedback),

    # Transaction
    path('show_transaction/', customer_views.show_customer_transaction),

    # Withdraw - Deposit - Transfer
    path('money_withdraw/', customer_views.customer_money_withdraw),
    path('money_deposit/', customer_views.customer_money_deposit),
    path('money_transfer/', customer_views.transfer_money),

    # Profile
    path('customer_profile/', customer_views.show_customer_profile),
    path('customer_update_pass/', customer_views.update_customer_pass),

    # Profile
    path('show_bank/', customer_views.all_bank),

    # Notification
    path('customer_notification/', customer_views.notification_to_customer),
]
