from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import TransactionType, AccountInterest, Bank


@receiver(post_migrate)
def create_transaction_types(sender, **kwargs):
    if sender.name == 'account_office_engine':
        transaction_types = [
            ('Bank Transfer', 'Transactions done via direct bank transfers.'),
            ('UPI', 'Transactions done through Unified Payments Interface (UPI).'),
            ('Cheque', 'Transactions done through Cheques.'),
            ('Credit Card', 'Transactions done using credit cards.'),
            ('Debit Card', 'Transactions done using debit cards.'),
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


@receiver(post_migrate)
def create_account_interests(sender, **kwargs):
    if sender.name == 'account_office_engine':
        account_interests = [
            (5, 3),
            (7, 6),
            (9, 12),
        ]

        for ai_rate, ai_amount_period in account_interests:
            AccountInterest.objects.get_or_create(
                ai_rate=ai_rate,
                ai_amount_period=ai_amount_period
            )


@receiver(post_migrate)
def create_default_banks(sender, **kwargs):
    if sender.name == 'account_office_engine':
        all_banks = [
            {"b_name": "ICICI", "b_city": "Mumbai", "b_area": "Andheri", "b_branch": "Andheri East",
             "b_address": "123 Andheri St", "b_pincode": "400053", "b_ifsc": "ICIC0001234"},
            {"b_name": "KOTAK", "b_city": "Delhi", "b_area": "Connaught Place", "b_branch": "Connaught Circle",
             "b_address": "456 CP Lane", "b_pincode": "110001", "b_ifsc": "KKBK0005678"},
            {"b_name": "SBI", "b_city": "Bangalore", "b_area": "MG Road", "b_branch": "MG Road Branch",
             "b_address": "789 MG Road", "b_pincode": "560001", "b_ifsc": "SBIN0004321"},
            {"b_name": "AXIS", "b_city": "Chennai", "b_area": "T Nagar", "b_branch": "T Nagar Branch",
             "b_address": "101 T Nagar St", "b_pincode": "600017", "b_ifsc": "UTIB0008765"},
            {"b_name": "HDFC", "b_city": "Pune", "b_area": "Shivaji Nagar", "b_branch": "Shivaji Nagar Branch",
             "b_address": "111 Shivaji St", "b_pincode": "411005", "b_ifsc": "HDFC0002345"},
            {"b_name": "PNB", "b_city": "Kolkata", "b_area": "Park Street", "b_branch": "Park Street Branch",
             "b_address": "222 Park St", "b_pincode": "700016", "b_ifsc": "PUNB0003456"},
            {"b_name": "BOB", "b_city": "Ahmedabad", "b_area": "CG Road", "b_branch": "CG Road Branch",
             "b_address": "333 CG Road", "b_pincode": "380009", "b_ifsc": "BARB0004567"},
            {"b_name": "YES", "b_city": "Hyderabad", "b_area": "Banjara Hills", "b_branch": "Banjara Hills Branch",
             "b_address": "444 Banjara Hills", "b_pincode": "500034", "b_ifsc": "YESB0005678"},
            {"b_name": "IDBI", "b_city": "Jaipur", "b_area": "MI Road", "b_branch": "MI Road Branch",
             "b_address": "555 MI Road", "b_pincode": "302001", "b_ifsc": "IBKL0006789"},
            {"b_name": "CANARA", "b_city": "Lucknow", "b_area": "Hazratganj", "b_branch": "Hazratganj Branch",
             "b_address": "666 Hazratganj", "b_pincode": "226001", "b_ifsc": "CNRB0007890"},
        ]

        for bank_data in all_banks:
            if not Bank.objects.filter(b_ifsc=bank_data["b_ifsc"]).exists():
                Bank.objects.create(**bank_data)
