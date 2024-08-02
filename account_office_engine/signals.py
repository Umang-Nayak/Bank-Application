from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import TransactionType


@receiver(post_migrate)
def create_transaction_types(sender, **kwargs):
    if sender.name == 'account_office_engine':
        transaction_types = [
            ('UPI', 'Transactions done through Unified Payments Interface (UPI).'),
            ('Cheque', 'Transactions done through Cheques.'),
            ('Credit Card', 'Transactions done using credit cards.'),
            ('Debit Card', 'Transactions done using debit cards.'),
            ('Bank Transfer', 'Transactions done via direct bank transfers.'),
            ('Cash', 'Transactions done using physical cash.'),
            ('Other Online Payment', 'Transactions done through various online payment gateways.'),
            ('Mobile Payment', 'Transactions done using mobile payment systems.'),
            ('Gift Card', 'Transactions involving the use of gift cards.'),
        ]

        for tt_type, tt_description in transaction_types:
            TransactionType.objects.get_or_create(
                tt_type=tt_type,
                defaults={'tt_description': tt_description}
            )
