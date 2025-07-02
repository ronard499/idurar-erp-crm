import os
import django
import bcrypt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idurar.settings')
django.setup()

from api.models import Admin, AdminPassword

# Check if superuser already exists
if not Admin.objects.filter(email='admin@example.com').exists():
    # Create superuser
    admin = Admin.objects.create(
        email='admin@example.com',
        name='Admin',
        surname='User',
        is_staff=True,
        is_superuser=True,
        is_active=True,
        enabled=True
    )
    
    # Set password
    password = 'admin123'
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    admin.password = hashed_password
    admin.save()
    
    # Create admin password record
    AdminPassword.objects.create(user=admin, logged_sessions=[])
    
    print(f"Superuser created with email: admin@example.com and password: {password}")
else:
    print("Superuser already exists")