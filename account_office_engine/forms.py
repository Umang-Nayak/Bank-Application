from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from account_office_engine.models import Employee, Customer


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["e_name", "e_email", "e_password", "e_contact", "e_address"]

    def clean_e_password(self):
        password = self.cleaned_data.get('e_password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(e.messages)
        return password

    def clean_e_contact(self):
        contact = self.cleaned_data.get('e_contact')
        if len(contact) != 10 or not contact.isdigit():
            raise ValidationError("Contact number must be exactly 10 digits long and contain only digits.")
        return contact


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["e_name", "e_email", "e_contact", "e_address"]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["c_name", "c_email", "c_password", "c_contact", "c_address"]

    def clean_e_password(self):
        password = self.cleaned_data.get('c_password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(e.messages)
        return password

    def clean_e_contact(self):
        contact = self.cleaned_data.get('c_contact')
        if len(contact) != 10 or not contact.isdigit():
            raise ValidationError("Contact number must be exactly 10 digits long and contain only digits.")
        return contact
