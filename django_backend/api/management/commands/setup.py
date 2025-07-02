from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Admin, AdminPassword, Setting
import os
import json

class Command(BaseCommand):
    help = 'Setup initial data for the application'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting setup...'))
        
        # Create default admin user if not exists
        if not Admin.objects.filter(email='admin@demo.com').exists():
            admin = Admin.objects.create_user(
                email='admin@demo.com',
                password='admin123',
                name='Admin',
                surname='User',
                is_staff=True,
                is_superuser=True
            )
            
            # Create admin password record
            AdminPassword.objects.create(user=admin, logged_sessions=[])
            
            self.stdout.write(self.style.SUCCESS('Default admin user created'))
        else:
            self.stdout.write(self.style.SUCCESS('Default admin user already exists'))
        
        # Create default settings
        default_settings = {
            'company_name': {'value': 'IDURAR ERP CRM'},
            'company_address': {'value': '123 Business Avenue, London, UK'},
            'company_email': {'value': 'info@idurarapp.com'},
            'company_phone': {'value': '+44 123 456 789'},
            'company_website': {'value': 'https://idurarapp.com'},
            'company_tax_number': {'value': 'TAX-123456789'},
            'company_vat_number': {'value': 'VAT-123456789'},
            'company_reg_number': {'value': 'REG-123456789'},
            'company_bank_name': {'value': 'Bank of Business'},
            'company_bank_account': {'value': '123456789'},
            'company_bank_iban': {'value': 'IBAN-123456789'},
            'company_bank_swift': {'value': 'SWIFT-123456789'},
            'company_logo': {'value': 'logo.png'},
            'company_currency': {'value': 'USD'},
            'company_currency_symbol': {'value': '$'},
            'date_format': {'value': 'DD/MM/YYYY'},
            'default_tax_rate': {'value': 20},
            'default_payment_terms': {'value': 14},
            'default_invoice_due_days': {'value': 30},
            'default_quote_valid_days': {'value': 30},
            'last_invoice_number': {'value': 0},
            'last_quote_number': {'value': 0},
            'last_payment_number': {'value': 0},
        }
        
        for key, data in default_settings.items():
            Setting.objects.get_or_create(
                key=key,
                defaults={'value': data['value']}
            )
        
        self.stdout.write(self.style.SUCCESS('Default settings created'))
        self.stdout.write(self.style.SUCCESS('Setup completed successfully'))