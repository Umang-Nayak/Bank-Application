from django.db import models


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=100)
    u_contact = models.CharField(max_length=13)
    u_address = models.TextField()
    u_email = models.EmailField(max_length=100, null=False, blank=False)
    u_password = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = "user"

    def __str__(self):
        return f"{self.u_email}"
