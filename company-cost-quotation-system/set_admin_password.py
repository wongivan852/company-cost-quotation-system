import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotation_system.settings')
django.setup()

from django.contrib.auth.models import User

# Set admin password to 'admin123'
admin_user = User.objects.get(username='admin')
admin_user.set_password('admin123')
admin_user.save()

print("Admin password set to: admin123")
print("You can now login with username: admin, password: admin123")