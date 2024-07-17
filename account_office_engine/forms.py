from django import forms
from account_office_engine.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["u_name", "u_email", "u_password", "u_contact", "u_address"]
