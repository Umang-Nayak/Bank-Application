from django.db import models


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


class Account(models.Model):
    a_id = models.AutoField(primary_key=True)
    c_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    a_open_date = models.DateField(auto_now_add=True)
    a_balance = models.FloatField(default=0)

    class Meta:
        db_table = "account"

    def __str__(self):
        return f"{self.a_id} - {self.c_id.c_email} - {self.a_balance}"


class AccountInterest(models.Model):
    ai_id = models.AutoField(primary_key=True)
    ai_amount = models.FloatField()

    class Meta:
        db_table = "account_interest"

    def __str__(self):
        return f"{self.ai_id} - {self.ai_amount}"


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


class Transaction(models.Model):
    t_id = models.AutoField(primary_key=True)
    tt_id = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    t_amount = models.FloatField()
    t_date = models.DateField(auto_now_add=True)
    a_id = models.ForeignKey(Account, on_delete=models.CASCADE)

    # transfer_account_no = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        db_table = "transaction"

    def __str__(self):
        return f"{self.t_id} - {self.t_amount}"
