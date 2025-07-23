#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotation_system.settings')
django.setup()

from quotations.models import Quotation

try:
    quotation = Quotation.objects.get(quotation_number='Q2025-0003')
    print(f"=== QUOTATION {quotation.quotation_number} STATUS ===")
    print(f"Current Status: {quotation.status}")
    print(f"Created by: {quotation.created_by.username} ({quotation.created_by.get_full_name()})")
    
    print(f"\n=== APPROVAL STATUS ===")
    print(f"1. Sales Staff Approved: {quotation.sales_staff_approved} | Date: {quotation.sales_staff_review_date}")
    print(f"2. Sales Manager Approved: {quotation.sales_manager_approved} | Date: {quotation.sales_manager_review_date}")
    print(f"3. Technical Approved: {quotation.technical_feasibility_approved} | Date: {quotation.technical_review_date}")
    print(f"4. Financial Approved: {quotation.financial_approved} | Date: {quotation.financial_review_date}")
    print(f"5. General Manager Approved: {quotation.general_manager_approved} | Date: {quotation.final_approval_date}")
    
    print(f"\n=== LEGACY FIELDS ===")
    print(f"Sales Supervisor Approved (legacy): {quotation.sales_supervisor_approved}")
    print(f"Sales Review Date (legacy): {quotation.sales_review_date}")
    
    print(f"\n=== WORKFLOW ANALYSIS ===")
    if quotation.status == 'draft':
        print("Status: Draft - Sales staff needs to submit for approval")
    elif quotation.status == 'pending_approval':
        if not quotation.sales_staff_approved:
            print("Current Step: Sales staff approval needed")
        elif not quotation.sales_manager_approved:
            print("Current Step: Sales manager approval needed")
        elif not quotation.technical_feasibility_approved:
            print("Current Step: Technical manager approval needed")
        elif not quotation.financial_approved:
            print("Current Step: Financial manager approval needed")
        elif not quotation.general_manager_approved:
            print("Current Step: General manager approval needed")
        else:
            print("ERROR: All approvals complete but status not 'approved'")
    elif quotation.status == 'approved':
        print("Status: Fully approved")
    else:
        print(f"Status: {quotation.status}")
    
    print(f"\n=== EXPECTED WORKFLOW STATE ===")
    if quotation.sales_manager_approved and not quotation.technical_feasibility_approved:
        print("✅ Sales Manager has approved")
        print("⏳ SHOULD BE: Awaiting Technical Manager approval")
        print("❌ ISSUE: If showing 'submitted' to Technical Manager, there's a workflow bug")
        
except Quotation.DoesNotExist:
    print("Quotation Q2025-0003 not found")
    # Show all quotations
    quotations = Quotation.objects.all().order_by('-created_at')
    print("All quotations:")
    for q in quotations:
        print(f"- {q.quotation_number}: {q.status}, created by {q.created_by.username}")