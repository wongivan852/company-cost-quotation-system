#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotation_system.settings')
django.setup()

from django.contrib.auth.models import User, Group

print("=== FIXING USER GROUPS FOR APPROVAL WORKFLOW ===")

# Create the required groups
required_groups = [
    'Sales Staff',
    'Sales Manager', 
    'Technical Manager',
    'Financial Manager',
    'General Manager'
]

print("Creating required groups...")
for group_name in required_groups:
    group, created = Group.objects.get_or_create(name=group_name)
    if created:
        print(f"✅ Created group: {group_name}")
    else:
        print(f"✅ Group exists: {group_name}")

print("\nAssigning users to correct groups...")

# Clear existing group assignments and assign correct ones
users_groups = {
    'sales_staff': ['Sales Staff'],
    'sales_manager': ['Sales Manager'],
    'technical_manager': ['Technical Manager'], 
    'finance_manager': ['Financial Manager'],
    'general_manager': ['General Manager']
}

for username, group_names in users_groups.items():
    try:
        user = User.objects.get(username=username)
        # Clear existing groups
        user.groups.clear()
        # Add correct groups
        for group_name in group_names:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        print(f"✅ {username} → {group_names}")
    except User.DoesNotExist:
        print(f"❌ User {username} not found")

print("\n=== VERIFICATION ===")
users = User.objects.all()
for user in users:
    user_groups = [g.name for g in user.groups.all()]
    print(f"{user.username}: {user_groups}")

print("\n=== CHECKING Q2025-0003 CREATOR ===")
try:
    from quotations.models import Quotation
    q = Quotation.objects.get(quotation_number='Q2025-0003')
    creator_groups = [g.name for g in q.created_by.groups.all()]
    print(f"Q2025-0003 creator ({q.created_by.username}) groups: {creator_groups}")
    
    if 'Sales Manager' in creator_groups:
        print("✅ Creator is Sales Manager - can approve sales manager step")
        print("⚠️  Issue: Sales Manager created quotation, but should Sales Staff approve first?")
        print("💡 Solution: Allow Sales Manager to skip Sales Staff step if they created it")
    
except:
    print("Q2025-0003 not found")