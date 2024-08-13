from django.db import models
from django.db import models, transaction
from django.core.exceptions import ValidationError


class Employee(models.Model):
    e_id = models.AutoField(primary_key=True)
    e_name = models.CharField(max_length=100)
    e_contact = models.CharField(max_length=13)
    e_address = models.TextField()
    e_email = models.EmailField(max_length=100, null=False, blank=False)
    e_password = models.CharField(max_length=50, null=False, blank=False)
    otp = models.CharField(max_length=10, null=True, blank=True)
    otp_used = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        db_table = "employee"

    def __str__(self):
        return f"{self.e_id} - {self.e_name} - {self.e_email}"


class Customer(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=100)
    c_contact = models.CharField(max_length=13)
    c_address = models.TextField()
    c_email = models.EmailField(max_length=100, null=False, blank=False)
    c_password = models.CharField(max_length=50, null=False, blank=False)
    otp = models.CharField(max_length=10, null=True, blank=True)
    otp_used = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        db_table = "customer"

    def __str__(self):
        return f"{self.c_id} - {self.c_name} - {self.c_email}"


class TransactionType(models.Model):
    tt_id = models.AutoField(primary_key=True)
    tt_type = models.CharField(max_length=100)
    tt_description = models.TextField()

    class Meta:
        db_table = "transaction_type"

    def __str__(self):
        return f"{self.tt_type}"


class AccountInterest(models.Model):
    ai_id = models.AutoField(primary_key=True)
    ai_rate = models.FloatField()
    ai_amount_period = models.IntegerField()

    class Meta:
        db_table = "account_interest"

    def __str__(self):
        return f"{self.ai_id} - {self.ai_rate} - {self.ai_amount_period}"


class Feedback(models.Model):
    f_id = models.AutoField(primary_key=True)
    f_description = models.TextField()
    f_date = models.DateField(auto_now_add=True)
    c_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        db_table = "feedback"

    def __str__(self):
        return f"{self.f_id} - {self.f_description} - {self.c_id.c_name}"


class Notification(models.Model):
    n_id = models.AutoField(primary_key=True)
    n_description = models.TextField()
    n_date = models.DateField(auto_now_add=True)
    c_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        db_table = "notification"

    def __str__(self):
        return f"{self.n_description} - {self.c_id.c_name}"


class Bank(models.Model):
    b_id = models.AutoField(primary_key=True)
    b_name = models.CharField(max_length=500, null=False, blank=False)
    b_city = models.CharField(max_length=500, null=False, blank=False)
    b_area = models.CharField(max_length=500, null=False, blank=False)
    b_branch = models.CharField(max_length=500, null=False, blank=False)
    b_address = models.CharField(max_length=500, null=False, blank=False)
    b_pincode = models.CharField(max_length=500, null=False, blank=False)
    b_ifsc = models.CharField(max_length=500, null=False, blank=False)

    class Meta:
        db_table = "bank"

    def __str__(self):
        return f"{self.b_name} - {self.b_ifsc}"


class Account(models.Model):
    a_id = models.AutoField(primary_key=True)
    c_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    a_open_date = models.DateField(auto_now_add=True)
    a_balance = models.FloatField(default=0)
    b_id = models.ForeignKey(Bank, on_delete=models.CASCADE)

    class Meta:
        db_table = "account"

    def __str__(self):
        return f"{self.a_id} - {self.c_id.c_email} - {self.a_balance}"


class Transaction(models.Model):
    t_id = models.AutoField(primary_key=True)
    tt_id = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    t_amount = models.FloatField()
    t_date = models.DateField(auto_now_add=True)
    a_id = models.ForeignKey(Account, related_name='source_account', on_delete=models.CASCADE)
    transfer_account_no = models.ForeignKey(Account, related_name='destination_account', on_delete=models.CASCADE)

    class Meta:
        db_table = "transaction"

    def __str__(self):
        return f"{self.t_id} - {self.t_amount}"

    def save(self, *args, **kwargs):
        # Ensure atomic transactions for balance updates
        with transaction.atomic():
            # Fetch the source and destination accounts
            source_account = self.a_id
            destination_account = self.transfer_account_no

            # Ensure source account has sufficient balance
            if source_account.a_balance < self.t_amount:
                raise ValidationError('Insufficient balance in the source account.')

            # Update balances
            source_account.a_balance -= self.t_amount
            destination_account.a_balance += self.t_amount

            # Save the updated accounts
            source_account.save()
            destination_account.save()

            # Call the superclass save method
            super().save(*args, **kwargs)


class InterestToCustomer(models.Model):
    ic_id = models.AutoField(primary_key=True)
    ic_amount_pay = models.FloatField()
    ic_amount_added_date = models.DateField(auto_now_add=True)
    a_id = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        db_table = "interest_to_customer"

    def __str__(self):
        return f"{self.ic_amount_pay} - {self.ic_amount_added_date} - {self.a_id}"
