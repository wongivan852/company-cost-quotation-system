#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotation_system.settings')
django.setup()

from quotations.models import Quotation
from django.utils import timezone

try:
    quotation = Quotation.objects.get(quotation_number='Q2025-0003')
    print(f"=== FIXING QUOTATION {quotation.quotation_number} ===")
    print(f"Creator: {quotation.created_by.username}")
    creator_groups = [g.name for g in quotation.created_by.groups.all()]
    print(f"Creator Groups: {creator_groups}")
    
    print(f"\nBefore Fix:")
    print(f"Sales Staff Approved: {quotation.sales_staff_approved}")
    print(f"Sales Manager Approved: {quotation.sales_manager_approved}")
    
    if 'Sales Manager' in creator_groups:
        # Since Sales Manager created it, both steps should be approved
        current_time = timezone.now()
        
        if not quotation.sales_manager_approved:
            quotation.sales_manager_approved = True
            quotation.sales_manager_review_date = current_time
            quotation.save()
            
            print(f"\nAfter Fix:")
            print(f"Sales Staff Approved: {quotation.sales_staff_approved}")
            print(f"Sales Manager Approved: {quotation.sales_manager_approved}")
            print(f"Sales Manager Review Date: {quotation.sales_manager_review_date}")
            print(f"\n✅ Fixed! Next step: Technical Manager approval")
        else:
            print("\n✅ Already in correct state")
    else:
        print(f"\n⚠️  Unexpected: Creator is not Sales Manager")
        
except Quotation.DoesNotExist:
    print("Quotation Q2025-0003 not found")