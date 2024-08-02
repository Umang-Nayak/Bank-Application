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

]
