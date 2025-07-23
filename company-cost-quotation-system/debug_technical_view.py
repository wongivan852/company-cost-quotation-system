#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotation_system.settings')
django.setup()

from quotations.models import Quotation
from django.contrib.auth.models import User

try:
    quotation = Quotation.objects.get(quotation_number='Q2025-0004')
    technical_manager = User.objects.get(username='technical_manager')
    
    print(f"=== TECHNICAL MANAGER VIEW FOR {quotation.quotation_number} ===")
    print(f"Technical Manager User: {technical_manager.username}")
    print(f"Technical Manager Groups: {[g.name for g in technical_manager.groups.all()]}")
    
    print(f"\n=== QUOTATION CONDITIONS ===")
    print(f"Status: {quotation.status}")
    print(f"Sales Staff Approved: {quotation.sales_staff_approved}")
    print(f"Sales Manager Approved: {quotation.sales_manager_approved}")
    print(f"Technical Approved: {quotation.technical_feasibility_approved}")
    
    print(f"\n=== TEMPLATE CONDITION CHECK ===")
    # Check template condition: 'Technical Manager' in user.groups.all|join:','
    user_groups_join = ','.join([g.name for g in technical_manager.groups.all()])
    print(f"user.groups.all|join:',': '{user_groups_join}'")
    print(f"'Technical Manager' in user.groups.all|join:',': {'Technical Manager' in user_groups_join}")
    
    # Check all conditions from template line 435
    condition1 = 'Technical Manager' in user_groups_join
    condition2 = quotation.sales_staff_approved
    condition3 = quotation.sales_manager_approved  
    condition4 = not quotation.technical_feasibility_approved
    
    print(f"\nTemplate conditions for Technical Manager approval button:")
    print(f"1. 'Technical Manager' in user.groups.all|join:',': {condition1}")
    print(f"2. quotation.sales_staff_approved: {condition2}")
    print(f"3. quotation.sales_manager_approved: {condition3}")
    print(f"4. not quotation.technical_feasibility_approved: {condition4}")
    
    all_conditions_met = condition1 and condition2 and condition3 and condition4
    print(f"\n✅ ALL CONDITIONS MET: {all_conditions_met}")
    
    if all_conditions_met:
        print("🎯 Technical Manager SHOULD see the approval button!")
    else:
        print("❌ Technical Manager should NOT see the approval button")
        print("   The quotation should show 'Waiting for appropriate approver to review.'")
        
except Quotation.DoesNotExist:
    print("Quotation Q2025-0004 not found")
except User.DoesNotExist:
    print("User technical_manager not found")