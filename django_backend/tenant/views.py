from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Client, Domain
from .serializers import ClientSerializer, DomainSerializer
from django.db import transaction


@api_view(['POST'])
@permission_classes([AllowAny])
def create_tenant(request):
    """
    Create a new tenant (business account)
    """
    try:
        with transaction.atomic():
            # Extract data from request
            name = request.data.get('name')
            schema_name = request.data.get('schema_name')
            domain_name = request.data.get('domain_name')
            
            # Validate required fields
            if not all([name, schema_name, domain_name]):
                return Response(
                    {'error': 'Name, schema_name, and domain_name are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if schema_name already exists
            if Client.objects.filter(schema_name=schema_name).exists():
                return Response(
                    {'error': 'A tenant with this schema name already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create the tenant
            tenant = Client(
                name=name,
                schema_name=schema_name,
                on_trial=True
            )
            tenant.save()
            
            # Add domain for the tenant
            domain = Domain()
            domain.domain = domain_name
            domain.tenant = tenant
            domain.is_primary = True
            domain.save()
            
            return Response(
                {
                    'success': True,
                    'message': 'Tenant created successfully',
                    'tenant': {
                        'name': tenant.name,
                        'schema_name': tenant.schema_name,
                        'domain': domain.domain
                    }
                },
                status=status.HTTP_201_CREATED
            )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_tenants(request):
    """
    List all tenants (business accounts)
    """
    try:
        tenants = Client.objects.all()
        serializer = ClientSerializer(tenants, many=True)
        
        # Add domains to each tenant
        for tenant_data in serializer.data:
            tenant = Client.objects.get(schema_name=tenant_data['schema_name'])
            domains = Domain.objects.filter(tenant=tenant)
            domain_serializer = DomainSerializer(domains, many=True)
            tenant_data['domains'] = domain_serializer.data
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
