import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotation_system.settings')
django.setup()

from django.contrib.auth.models import User

# Set sales_manager password to 'manager123'
try:
    sales_manager_user = User.objects.get(username='sales_manager')
    sales_manager_user.set_password('manager123')
    sales_manager_user.save()
    
    print("Sales manager password set to: manager123")
    print("You can now login with username: sales_manager, password: manager123")
except User.DoesNotExist:
    print("Error: sales_manager user does not exist")
