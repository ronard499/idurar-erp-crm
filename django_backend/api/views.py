from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
import datetime
import json

from .models import (
    Admin, Client, PaymentMode, Product, Quote, QuoteItem,
    Invoice, InvoiceItem, Payment, Setting
)
from .serializers import (
    AdminSerializer, AdminCreateSerializer, ClientSerializer,
    PaymentModeSerializer, ProductSerializer, QuoteSerializer,
    QuoteCreateSerializer, InvoiceSerializer, InvoiceCreateSerializer,
    PaymentSerializer, PaymentCreateSerializer, SettingSerializer
)

# Helper functions
def calculate_pagination(page, limit, count):
    pages = (count + limit - 1) // limit
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < pages else None
    
    return {
        'page': page,
        'limit': limit,
        'pages': pages,
        'total': count,
        'prev': prev_page,
        'next': next_page,
    }

def get_filter_options(request, model):
    filter_options = {}
    
    # Common filters for all models
    filter_options['removed'] = False
    
    # Get filter parameter
    filter_param = request.query_params.get('filter')
    equal_param = request.query_params.get('equal')
    
    if filter_param and equal_param:
        filter_options[filter_param] = equal_param
    
    return filter_options

def search_model(request, model, search_fields):
    query = request.query_params.get('q', '')
    
    if not query:
        return model.objects.filter(removed=False)
    
    q_objects = Q()
    for field in search_fields:
        q_objects |= Q(**{f"{field}__icontains": query})
    
    return model.objects.filter(q_objects, removed=False)

# Generic CRUD views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request, model, serializer_class, create_serializer_class=None):
    if create_serializer_class is None:
        create_serializer_class = serializer_class
    
    # Add created_by field if it exists in the model
    if hasattr(model, 'created_by'):
        request.data['created_by'] = request.user.id
    
    serializer = create_serializer_class(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'result': serializer.data,
            'message': f"{model.__name__} created successfully",
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'result': None,
        'message': serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_item(request, id, model, serializer_class):
    item = get_object_or_404(model, id=id, removed=False)
    serializer = serializer_class(item)
    
    return Response({
        'success': True,
        'result': serializer.data,
        'message': f"{model.__name__} retrieved successfully",
    }, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_item(request, id, model, serializer_class):
    item = get_object_or_404(model, id=id, removed=False)
    serializer = serializer_class(item, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'result': serializer.data,
            'message': f"{model.__name__} updated successfully",
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'result': None,
        'message': serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request, id, model, serializer_class):
    item = get_object_or_404(model, id=id, removed=False)
    
    # Soft delete
    item.removed = True
    item.save()
    
    serializer = serializer_class(item)
    
    return Response({
        'success': True,
        'result': serializer.data,
        'message': f"{model.__name__} deleted successfully",
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_items(request, model, serializer_class, search_fields=None):
    page = int(request.query_params.get('page', 1))
    limit = int(request.query_params.get('limit', 10))
    
    # Apply filters
    filter_options = get_filter_options(request, model)
    
    # Apply search if search_fields provided
    if search_fields and request.query_params.get('q'):
        queryset = search_model(request, model, search_fields)
    else:
        queryset = model.objects.filter(**filter_options)
    
    # Calculate total count
    count = queryset.count()
    
    # Apply pagination
    start = (page - 1) * limit
    end = page * limit
    queryset = queryset.order_by('-created')[start:end]
    
    serializer = serializer_class(queryset, many=True)
    
    pagination = calculate_pagination(page, limit, count)
    
    return Response({
        'success': True,
        'result': serializer.data,
        'pagination': pagination,
        'message': f"{model.__name__} list retrieved successfully",
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_items(request, model, serializer_class):
    queryset = model.objects.filter(removed=False)
    serializer = serializer_class(queryset, many=True)
    
    return Response({
        'success': True,
        'result': serializer.data,
        'message': f"All {model.__name__} retrieved successfully",
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_items(request, model, serializer_class):
    filter_options = get_filter_options(request, model)
    queryset = model.objects.filter(**filter_options)
    serializer = serializer_class(queryset, many=True)
    
    return Response({
        'success': True,
        'result': serializer.data,
        'message': f"Filtered {model.__name__} retrieved successfully",
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_items(request, model, serializer_class, search_fields):
    queryset = search_model(request, model, search_fields)
    serializer = serializer_class(queryset, many=True)
    
    return Response({
        'success': True,
        'result': serializer.data,
        'message': f"Search results for {model.__name__}",
    }, status=status.HTTP_200_OK)

# Client views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_client(request):
    return create_item(request, Client, ClientSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_client(request, id):
    return read_item(request, id, Client, ClientSerializer)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_client(request, id):
    return update_item(request, id, Client, ClientSerializer)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_client(request, id):
    return delete_item(request, id, Client, ClientSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_clients(request):
    return list_items(request, Client, ClientSerializer, ['name', 'email', 'phone'])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_clients(request):
    return list_all_items(request, Client, ClientSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_clients(request):
    return filter_items(request, Client, ClientSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_clients(request):
    return search_items(request, Client, ClientSerializer, ['name', 'email', 'phone'])

# PaymentMode views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_mode(request):
    return create_item(request, PaymentMode, PaymentModeSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_payment_mode(request, id):
    return read_item(request, id, PaymentMode, PaymentModeSerializer)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_payment_mode(request, id):
    return update_item(request, id, PaymentMode, PaymentModeSerializer)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_payment_mode(request, id):
    return delete_item(request, id, PaymentMode, PaymentModeSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_payment_modes(request):
    return list_items(request, PaymentMode, PaymentModeSerializer, ['name'])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_payment_modes(request):
    return list_all_items(request, PaymentMode, PaymentModeSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_payment_modes(request):
    return filter_items(request, PaymentMode, PaymentModeSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_payment_modes(request):
    return search_items(request, PaymentMode, PaymentModeSerializer, ['name'])

# Product views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    return create_item(request, Product, ProductSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_product(request, id):
    return read_item(request, id, Product, ProductSerializer)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_product(request, id):
    return update_item(request, id, Product, ProductSerializer)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, id):
    return delete_item(request, id, Product, ProductSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_products(request):
    return list_items(request, Product, ProductSerializer, ['name', 'reference'])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_products(request):
    return list_all_items(request, Product, ProductSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_products(request):
    return filter_items(request, Product, ProductSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_products(request):
    return search_items(request, Product, ProductSerializer, ['name', 'reference'])

# Quote views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_quote(request):
    return create_item(request, Quote, QuoteSerializer, QuoteCreateSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_quote(request, id):
    return read_item(request, id, Quote, QuoteSerializer)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_quote(request, id):
    return update_item(request, id, Quote, QuoteSerializer)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_quote(request, id):
    return delete_item(request, id, Quote, QuoteSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_quotes(request):
    return list_items(request, Quote, QuoteSerializer, ['number'])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_quotes(request):
    return list_all_items(request, Quote, QuoteSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_quotes(request):
    return filter_items(request, Quote, QuoteSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_quotes(request):
    return search_items(request, Quote, QuoteSerializer, ['number'])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def convert_quote_to_invoice(request, id):
    quote = get_object_or_404(Quote, id=id, removed=False)
    
    # Create invoice from quote
    invoice_data = {
        'number': quote.number,
        'year': quote.year,
        'date': quote.date,
        'expiry_date': quote.expiry_date,
        'client': quote.client.id,
        'sub_total': quote.sub_total,
        'tax_rate': quote.tax_rate,
        'tax_total': quote.tax_total,
        'discount': quote.discount,
        'total': quote.total,
        'credit': 0,
        'note': quote.note,
        'status': 'draft',
        'quote': quote.id,
        'created_by': request.user.id,
    }
    
    # Get quote items
    quote_items = QuoteItem.objects.filter(quote=quote)
    
    # Create invoice items
    invoice_items = []
    for item in quote_items:
        invoice_items.append({
            'product': item.product.id if item.product else None,
            'name': item.name,
            'description': item.description,
            'quantity': item.quantity,
            'price': item.price,
            'total': item.total,
        })
    
    # Create invoice
    invoice_data['items'] = invoice_items
    serializer = InvoiceCreateSerializer(data=invoice_data)
    
    if serializer.is_valid():
        invoice = serializer.save()
        return Response({
            'success': True,
            'result': InvoiceSerializer(invoice).data,
            'message': 'Quote converted to invoice successfully',
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'result': None,
        'message': serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)

# Invoice views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_invoice(request):
    return create_item(request, Invoice, InvoiceSerializer, InvoiceCreateSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_invoice(request, id):
    return read_item(request, id, Invoice, InvoiceSerializer)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_invoice(request, id):
    return update_item(request, id, Invoice, InvoiceSerializer)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_invoice(request, id):
    return delete_item(request, id, Invoice, InvoiceSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_invoices(request):
    return list_items(request, Invoice, InvoiceSerializer, ['number'])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_invoices(request):
    return list_all_items(request, Invoice, InvoiceSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_invoices(request):
    return filter_items(request, Invoice, InvoiceSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_invoices(request):
    return search_items(request, Invoice, InvoiceSerializer, ['number'])

# Payment views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    return create_item(request, Payment, PaymentSerializer, PaymentCreateSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_payment(request, id):
    return read_item(request, id, Payment, PaymentSerializer)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_payment(request, id):
    return update_item(request, id, Payment, PaymentSerializer)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_payment(request, id):
    return delete_item(request, id, Payment, PaymentSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_payments(request):
    return list_items(request, Payment, PaymentSerializer, ['number'])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_payments(request):
    return list_all_items(request, Payment, PaymentSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_payments(request):
    return filter_items(request, Payment, PaymentSerializer)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_payments(request):
    return search_items(request, Payment, PaymentSerializer, ['number'])

# Summary views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_summary(request):
    total_clients = Client.objects.filter(removed=False).count()
    
    return Response({
        'success': True,
        'result': {
            'total': total_clients,
        },
        'message': 'Client summary retrieved successfully',
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def invoice_summary(request):
    # Get query parameters
    year = request.query_params.get('year', datetime.datetime.now().year)
    month = request.query_params.get('month')
    
    # Base query
    query = Q(removed=False)
    
    # Add year filter
    if year:
        query &= Q(year=year)
    
    # Add month filter if provided
    if month:
        query &= Q(date__month=month)
    
    # Get invoices
    invoices = Invoice.objects.filter(query)
    
    # Calculate totals
    total_count = invoices.count()
    total_amount = invoices.aggregate(Sum('total'))['total__sum'] or 0
    paid_amount = invoices.aggregate(Sum('credit'))['credit__sum'] or 0
    unpaid_amount = total_amount - paid_amount
    
    # Calculate status counts
    draft_count = invoices.filter(status='draft').count()
    pending_count = invoices.filter(status='pending').count()
    paid_count = invoices.filter(status='paid').count()
    
    return Response({
        'success': True,
        'result': {
            'total': total_count,
            'total_amount': total_amount,
            'paid_amount': paid_amount,
            'unpaid_amount': unpaid_amount,
            'draft_count': draft_count,
            'pending_count': pending_count,
            'paid_count': paid_count,
        },
        'message': 'Invoice summary retrieved successfully',
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quote_summary(request):
    # Get query parameters
    year = request.query_params.get('year', datetime.datetime.now().year)
    month = request.query_params.get('month')
    
    # Base query
    query = Q(removed=False)
    
    # Add year filter
    if year:
        query &= Q(year=year)
    
    # Add month filter if provided
    if month:
        query &= Q(date__month=month)
    
    # Get quotes
    quotes = Quote.objects.filter(query)
    
    # Calculate totals
    total_count = quotes.count()
    total_amount = quotes.aggregate(Sum('total'))['total__sum'] or 0
    
    # Calculate status counts
    draft_count = quotes.filter(status='draft').count()
    pending_count = quotes.filter(status='pending').count()
    sent_count = quotes.filter(status='sent').count()
    
    return Response({
        'success': True,
        'result': {
            'total': total_count,
            'total_amount': total_amount,
            'draft_count': draft_count,
            'pending_count': pending_count,
            'sent_count': sent_count,
        },
        'message': 'Quote summary retrieved successfully',
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_summary(request):
    # Get query parameters
    year = request.query_params.get('year', datetime.datetime.now().year)
    month = request.query_params.get('month')
    
    # Base query
    query = Q(removed=False)
    
    # Add year filter
    if year:
        query &= Q(year=year)
    
    # Add month filter if provided
    if month:
        query &= Q(date__month=month)
    
    # Get payments
    payments = Payment.objects.filter(query)
    
    # Calculate totals
    total_count = payments.count()
    total_amount = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    
    return Response({
        'success': True,
        'result': {
            'total': total_count,
            'total_amount': total_amount,
        },
        'message': 'Payment summary retrieved successfully',
    }, status=status.HTTP_200_OK)

# Settings views
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def settings(request, key=None):
    if request.method == 'GET':
        if key:
            # Get specific setting
            setting = get_object_or_404(Setting, key=key)
            serializer = SettingSerializer(setting)
            return Response({
                'success': True,
                'result': serializer.data,
                'message': 'Setting retrieved successfully',
            }, status=status.HTTP_200_OK)
        else:
            # Get all settings
            settings = Setting.objects.all()
            serializer = SettingSerializer(settings, many=True)
            return Response({
                'success': True,
                'result': serializer.data,
                'message': 'Settings retrieved successfully',
            }, status=status.HTTP_200_OK)
    
    elif request.method == 'PATCH':
        if not key:
            return Response({
                'success': False,
                'result': None,
                'message': 'Setting key is required',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create setting
        setting, created = Setting.objects.get_or_create(key=key)
        
        # Update value
        value = request.data.get('value')
        if value is None:
            return Response({
                'success': False,
                'result': None,
                'message': 'Value is required',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        setting.value = value
        setting.save()
        
        serializer = SettingSerializer(setting)
        return Response({
            'success': True,
            'result': serializer.data,
            'message': 'Setting updated successfully',
        }, status=status.HTTP_200_OK)

# Mail views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mail_invoice(request):
    # In a real application, this would send an email with the invoice
    # For now, we'll just return a success response
    
    return Response({
        'success': True,
        'result': None,
        'message': 'Invoice email sent successfully',
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mail_quote(request):
    # In a real application, this would send an email with the quote
    # For now, we'll just return a success response
    
    return Response({
        'success': True,
        'result': None,
        'message': 'Quote email sent successfully',
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mail_payment(request):
    # In a real application, this would send an email with the payment receipt
    # For now, we'll just return a success response
    
    return Response({
        'success': True,
        'result': None,
        'message': 'Payment receipt email sent successfully',
    }, status=status.HTTP_200_OK)
