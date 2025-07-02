from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Client(TenantMixin):
    """
    Tenant model for multi-tenancy support.
    Each client represents a separate business account.
    """
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    
    # Default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
    
    def __str__(self):
        return self.name


class Domain(DomainMixin):
    """
    Domain model for multi-tenancy support.
    Each domain is associated with a tenant.
    """
    pass
