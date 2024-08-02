from django.contrib import admin
from account_office_engine.models import (Employee, Customer, TransactionType,
                                          Account, AccountInterest, Feedback,
                                          Notification, Transaction)

admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(TransactionType)
admin.site.register(Account)
admin.site.register(AccountInterest)
admin.site.register(Feedback)
admin.site.register(Notification)
admin.site.register(Transaction)
