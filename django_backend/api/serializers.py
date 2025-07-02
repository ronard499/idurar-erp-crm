from rest_framework import serializers
from .models import (
    Admin, AdminPassword, Client, PaymentMode, Product, 
    Quote, QuoteItem, Invoice, InvoiceItem, Payment, Setting
)
from django.contrib.auth.hashers import make_password
import uuid

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'email', 'name', 'surname', 'photo', 'enabled', 'created', 'updated']
        read_only_fields = ['id', 'created', 'updated']

class AdminCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Admin
        fields = ['id', 'email', 'name', 'surname', 'password', 'photo', 'enabled']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        admin = Admin.objects.create(**validated_data)
        admin.set_password(password)
        admin.save()
        
        # Create AdminPassword record
        AdminPassword.objects.create(user=admin, logged_sessions=[])
        
        return admin

class ClientSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()
    assigned_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = ['id', 'name', 'phone', 'country', 'address', 'email', 
                  'created_by', 'created_by_name', 'assigned', 'assigned_name', 
                  'enabled', 'removed', 'created', 'updated']
        read_only_fields = ['id', 'created', 'updated', 'created_by_name', 'assigned_name']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.name
        return None
    
    def get_assigned_name(self, obj):
        if obj.assigned:
            return obj.assigned.name
        return None

class PaymentModeSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = PaymentMode
        fields = ['id', 'name', 'description', 'created_by', 'created_by_name', 
                  'enabled', 'removed', 'created', 'updated']
        read_only_fields = ['id', 'created', 'updated', 'created_by_name']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.name
        return None

class ProductSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'reference', 'description', 'price', 
                  'created_by', 'created_by_name', 'enabled', 'removed', 
                  'created', 'updated']
        read_only_fields = ['id', 'created', 'updated', 'created_by_name']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.name
        return None

class QuoteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteItem
        fields = ['id', 'quote', 'product', 'name', 'description', 
                  'quantity', 'price', 'total']
        read_only_fields = ['id']

class QuoteSerializer(serializers.ModelSerializer):
    items = QuoteItemSerializer(many=True, read_only=True)
    client_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Quote
        fields = ['id', 'number', 'year', 'date', 'expiry_date', 'client', 'client_name',
                  'sub_total', 'tax_rate', 'tax_total', 'discount', 'total',
                  'note', 'status', 'pdf', 'items', 'created_by', 'created_by_name',
                  'enabled', 'removed', 'created', 'updated']
        read_only_fields = ['id', 'created', 'updated', 'client_name', 'created_by_name']
    
    def get_client_name(self, obj):
        return obj.client.name if obj.client else None
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.name
        return None

class QuoteCreateSerializer(serializers.ModelSerializer):
    items = QuoteItemSerializer(many=True)
    
    class Meta:
        model = Quote
        fields = ['id', 'number', 'year', 'date', 'expiry_date', 'client',
                  'sub_total', 'tax_rate', 'tax_total', 'discount', 'total',
                  'note', 'status', 'items', 'created_by']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        quote = Quote.objects.create(**validated_data)
        
        for item_data in items_data:
            QuoteItem.objects.create(quote=quote, **item_data)
        
        # Generate PDF filename
        pdf_filename = f"quote-{quote.id}.pdf"
        quote.pdf = pdf_filename
        quote.save()
        
        return quote

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'invoice', 'product', 'name', 'description', 
                  'quantity', 'price', 'total']
        read_only_fields = ['id']

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    client_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = ['id', 'number', 'year', 'date', 'expiry_date', 'client', 'client_name',
                  'sub_total', 'tax_rate', 'tax_total', 'discount', 'total', 'credit',
                  'note', 'status', 'pdf', 'quote', 'items', 'created_by', 'created_by_name',
                  'enabled', 'removed', 'created', 'updated']
        read_only_fields = ['id', 'created', 'updated', 'client_name', 'created_by_name']
    
    def get_client_name(self, obj):
        return obj.client.name if obj.client else None
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.name
        return None

class InvoiceCreateSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    
    class Meta:
        model = Invoice
        fields = ['id', 'number', 'year', 'date', 'expiry_date', 'client',
                  'sub_total', 'tax_rate', 'tax_total', 'discount', 'total', 'credit',
                  'note', 'status', 'quote', 'items', 'created_by']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        
        # Generate PDF filename
        pdf_filename = f"invoice-{invoice.id}.pdf"
        invoice.pdf = pdf_filename
        invoice.save()
        
        return invoice

class PaymentSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()
    invoice_number = serializers.SerializerMethodField()
    payment_mode_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = ['id', 'number', 'year', 'date', 'amount', 'payment_mode', 'payment_mode_name',
                  'invoice', 'invoice_number', 'client', 'client_name', 'note', 'ref', 'pdf',
                  'created_by', 'created_by_name', 'enabled', 'removed', 'created', 'updated']
        read_only_fields = ['id', 'created', 'updated', 'client_name', 'invoice_number', 
                           'payment_mode_name', 'created_by_name']
    
    def get_client_name(self, obj):
        return obj.client.name if obj.client else None
    
    def get_invoice_number(self, obj):
        return obj.invoice.number if obj.invoice else None
    
    def get_payment_mode_name(self, obj):
        return obj.payment_mode.name if obj.payment_mode else None
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.name
        return None

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'number', 'year', 'date', 'amount', 'payment_mode',
                  'invoice', 'client', 'note', 'ref', 'created_by']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        
        # Generate PDF filename
        pdf_filename = f"payment-{payment.id}.pdf"
        payment.pdf = pdf_filename
        payment.save()
        
        # Update invoice credit
        invoice = payment.invoice
        if invoice:
            invoice.credit = invoice.credit + payment.amount
            invoice.save()
        
        return payment

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['key', 'value']