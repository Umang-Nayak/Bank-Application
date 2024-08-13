from django.contrib import admin
from account_office_engine.models import (Employee, Customer, TransactionType,
                                          Account, AccountInterest, Feedback,
                                          Notification, Transaction, Bank)

from django.contrib import admin
from django.http import HttpResponse
import openpyxl
from io import BytesIO
from django.urls import path


def export_to_excel(queryset, filename):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Data'

    headers = [field.name for field in queryset.model._meta.fields]
    worksheet.append(headers)

    for obj in queryset:
        row = []
        for field in headers:
            value = getattr(obj, field)
            if isinstance(value, str):
                row.append(value)
            elif isinstance(value, (int, float)):
                row.append(value)
            elif value is None:
                row.append('')
            elif hasattr(value, '__str__'):
                row.append(str(value))
            else:
                row.append('')
        worksheet.append(row)

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
    return response


def export_employees_to_excel(modeladmin, request, queryset):
    return export_to_excel(queryset, 'employees')


def export_customers_to_excel(modeladmin, request, queryset):
    return export_to_excel(queryset, 'customers')


def export_accounts_to_excel(modeladmin, request, queryset):
    return export_to_excel(queryset, 'accounts')


def export_feedbacks_to_excel(modeladmin, request, queryset):
    return export_to_excel(queryset, 'feedbacks')


def export_transactions_to_excel(modeladmin, request, queryset):
    return export_to_excel(queryset, 'transactions')


export_employees_to_excel.short_description = 'Export selected employees to Excel'
export_customers_to_excel.short_description = 'Export selected customers to Excel'
export_accounts_to_excel.short_description = 'Export selected accounts to Excel'
export_feedbacks_to_excel.short_description = 'Export selected feedbacks to Excel'
export_transactions_to_excel.short_description = 'Export selected transactions to Excel'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Employee._meta.fields]
    actions = [export_employees_to_excel]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-all/', self.export_all_employees_to_excel, name='export_all_employees_to_excel'),
        ]
        return custom_urls + urls

    def export_all_employees_to_excel(self, request):
        queryset = Employee.objects.all()
        return export_employees_to_excel(self, request, queryset)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_all_url'] = 'export-all/'
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.fields]
    actions = [export_customers_to_excel]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-all/', self.export_all_customers_to_excel, name='export_all_customers_to_excel'),
        ]
        return custom_urls + urls

    def export_all_customers_to_excel(self, request):
        queryset = Customer.objects.all()
        return export_customers_to_excel(self, request, queryset)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_all_url'] = 'export-all/'
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Account._meta.fields]
    actions = [export_accounts_to_excel]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-all/', self.export_all_accounts_to_excel, name='export_all_accounts_to_excel'),
        ]
        return custom_urls + urls

    def export_all_accounts_to_excel(self, request):
        queryset = Account.objects.all()
        return export_accounts_to_excel(self, request, queryset)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_all_url'] = 'export-all/'
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Feedback._meta.fields]
    actions = [export_feedbacks_to_excel]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-all/', self.export_all_feedbacks_to_excel, name='export_all_feedbacks_to_excel'),
        ]
        return custom_urls + urls

    def export_all_feedbacks_to_excel(self, request):
        queryset = Feedback.objects.all()
        return export_feedbacks_to_excel(self, request, queryset)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_all_url'] = 'export-all/'
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Transaction._meta.fields]
    actions = [export_transactions_to_excel]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-all/', self.export_all_transactions_to_excel, name='export_all_transactions_to_excel'),
        ]
        return custom_urls + urls

    def export_all_transactions_to_excel(self, request):
        queryset = Transaction.objects.all()
        return export_transactions_to_excel(self, request, queryset)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['export_all_url'] = 'export-all/'
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(TransactionType)
admin.site.register(AccountInterest)
admin.site.register(Notification)
admin.site.register(Bank)
