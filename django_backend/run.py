#!/usr/bin/env python
import os
import sys
import dotenv
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    # Load environment variables from .env file
    dotenv.load_dotenv()
    
    # Set default settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idurar.settings')
    
    # Get port from environment or use default
    port = os.environ.get('PORT', '8888')
    
    # Run migrations
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Run setup command
    execute_from_command_line(['manage.py', 'setup'])
    
    # Run server
    execute_from_command_line(['manage.py', 'runserver', f'0.0.0.0:{port}'])