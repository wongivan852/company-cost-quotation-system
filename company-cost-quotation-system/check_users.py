#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotation_system.settings')
django.setup()

from django.contrib.auth.models import User, Group
from quotations.models import Quotation

print("=== USER GROUPS ANALYSIS ===")
groups = Group.objects.all()
for group in groups:
    users = group.user_set.all()
    print(f"\n{group.name} Group:")
    for user in users:
        print(f"  - {user.username} ({user.get_full_name() or 'No full name'})")

print("\n=== ALL USERS AND THEIR GROUPS ===")
users = User.objects.all()
for user in users:
    user_groups = [g.name for g in user.groups.all()]
    print(f"{user.username}: {user_groups}")

print("\n=== QUOTATION CREATORS ===")
quotations = Quotation.objects.all()
for q in quotations:
    creator_groups = [g.name for g in q.created_by.groups.all()]
    print(f"{q.quotation_number}: Created by {q.created_by.username} (Groups: {creator_groups})")

print("\n=== Q2025-0003 SPECIFIC ANALYSIS ===")
try:
    q = Quotation.objects.get(quotation_number='Q2025-0003')
    creator = q.created_by
    creator_groups = [g.name for g in creator.groups.all()]
    print(f"Creator: {creator.username}")
    print(f"Creator Groups: {creator_groups}")
    print(f"Sales Staff Approved: {q.sales_staff_approved}")
    print(f"Sales Manager Approved: {q.sales_manager_approved}")
    
    print("\nLogic Check:")
    if 'Sales Manager' in creator_groups:
        print("- Creator is Sales Manager")
        print("- Question: Can a Sales Manager approve their own quotation?")
        print("- Current logic: Sales Manager can only approve AFTER Sales Staff approval")
        print("- Issue: If Sales Manager created it, who does Sales Staff approval?")
except:
    print("Q2025-0003 not found")