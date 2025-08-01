import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotation_system.settings')
django.setup()

from django.contrib.auth.models import User

# Set technical_manager password to 'tech123'
try:
    technical_manager_user = User.objects.get(username='technical_manager')
    technical_manager_user.set_password('tech123')
    technical_manager_user.save()
    
    print("Technical manager password set to: tech123")
    print("You can now login with username: technical_manager, password: tech123")
except User.DoesNotExist:
    print("Error: technical_manager user does not exist")
