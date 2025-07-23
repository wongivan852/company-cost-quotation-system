from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import (
    Quotation, QuotationItem, QuotationApproval, CustomerQuotationRequest,
    Customer, Hardware, Service, PersonnelCostCategory, QuotationPersonnelCost, MarginAnalysis
)
from .forms import CustomerQuotationRequestForm, QuotationForm
from datetime import datetime, timedelta
import json


def customer_request(request):
    if request.method == 'POST':
        form = CustomerQuotationRequestForm(request.POST)
        if form.is_valid():
            customer_request = form.save()
            messages.success(
                request, 
                f'Your quotation request has been submitted successfully! '
                f'Reference: {customer_request.id}. We will contact you within 24-48 hours.'
            )
            return redirect('quotations:request_submitted', request_id=customer_request.id)
    else:
        form = CustomerQuotationRequestForm()
    
    return render(request, 'quotations/customer_request_form.html', {
        'form': form,
        'today': datetime.now().date()
    })


def request_submitted(request, request_id):
    customer_request = get_object_or_404(CustomerQuotationRequest, id=request_id)
    return render(request, 'quotations/request_submitted.html', {
        'request': customer_request
    })


@login_required
def dashboard(request):
    # Get counts for dashboard
    total_requests = CustomerQuotationRequest.objects.count()
    pending_requests = CustomerQuotationRequest.objects.filter(status='submitted').count()
    total_quotations = Quotation.objects.count()
    pending_quotations = Quotation.objects.filter(status='pending_approval').count()
    
    # Recent requests
    recent_requests = CustomerQuotationRequest.objects.select_related('assigned_sales_staff').order_by('-submitted_at')[:5]
    
    # Quotations needing user's attention (based on user role)
    user_quotations = []
    if request.user.groups.filter(name='Sales Staff').exists():
        # Show draft quotations created by this user + quotations pending their approval
        user_quotations = Quotation.objects.filter(
            Q(status='draft', created_by=request.user) |
            Q(status='pending_approval', created_by=request.user, sales_staff_approved=False)
        ).order_by('-created_at')[:5]
    elif request.user.groups.filter(name='Sales Manager').exists():
        # Show quotations pending sales manager approval
        user_quotations = Quotation.objects.filter(
            status='pending_approval',
            sales_staff_approved=True,
            sales_manager_approved=False
        ).order_by('-created_at')[:5]
    elif request.user.groups.filter(name='Technical Manager').exists():
        # Show quotations pending technical approval
        user_quotations = Quotation.objects.filter(
            status='pending_approval',
            sales_staff_approved=True,
            sales_manager_approved=True, 
            technical_feasibility_approved=False
        ).order_by('-created_at')[:5]
    elif request.user.groups.filter(name='Financial Manager').exists():
        # Show quotations pending financial approval
        user_quotations = Quotation.objects.filter(
            status='pending_approval',
            sales_staff_approved=True,
            sales_manager_approved=True,
            technical_feasibility_approved=True,
            financial_approved=False
        ).order_by('-created_at')[:5]
    elif request.user.groups.filter(name='General Manager').exists():
        # Show quotations pending final approval
        user_quotations = Quotation.objects.filter(
            status='pending_approval',
            sales_staff_approved=True,
            sales_manager_approved=True,
            technical_feasibility_approved=True,
            financial_approved=True,
            general_manager_approved=False
        ).order_by('-created_at')[:5]
    
    return render(request, 'quotations/dashboard.html', {
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'total_quotations': total_quotations,
        'pending_quotations': pending_quotations,
        'recent_requests': recent_requests,
        'user_quotations': user_quotations,
        'user': request.user,
    })


@login_required
def request_list(request):
    requests_qs = CustomerQuotationRequest.objects.select_related('assigned_sales_staff', 'existing_customer')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        requests_qs = requests_qs.filter(status=status)
    
    # Filter by priority
    priority = request.GET.get('priority')
    if priority:
        requests_qs = requests_qs.filter(priority=priority)
    
    # Search
    search = request.GET.get('search')
    if search:
        requests_qs = requests_qs.filter(
            Q(company_name__icontains=search) |
            Q(contact_person__icontains=search) |
            Q(project_title__icontains=search)
        )
    
    requests_qs = requests_qs.order_by('-submitted_at')
    
    return render(request, 'quotations/request_list.html', {
        'requests': requests_qs,
        'status_choices': CustomerQuotationRequest.STATUS_CHOICES,
        'priority_choices': CustomerQuotationRequest.PRIORITY_CHOICES,
        'current_status': status,
        'current_priority': priority,
        'search_query': search,
    })


@login_required
def request_detail(request, request_id):
    customer_request = get_object_or_404(
        CustomerQuotationRequest.objects.select_related('assigned_sales_staff', 'existing_customer', 'converted_quotation'),
        id=request_id
    )
    
    return render(request, 'quotations/request_detail.html', {
        'request': customer_request
    })


@login_required
def quotation_list(request):
    quotations = Quotation.objects.select_related('customer', 'created_by').all()
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        quotations = quotations.filter(status=status)
    
    # Search
    search = request.GET.get('search')
    if search:
        quotations = quotations.filter(
            Q(quotation_number__icontains=search) |
            Q(customer__company_name__icontains=search) |
            Q(title__icontains=search)
        )
    
    quotations = quotations.order_by('-created_at')
    
    return render(request, 'quotations/quotation_list.html', {
        'quotations': quotations,
        'status_choices': Quotation.STATUS_CHOICES,
        'current_status': status,
        'search_query': search,
    })


@login_required
def quotation_detail(request, quotation_id):
    quotation = get_object_or_404(
        Quotation.objects.select_related('customer', 'created_by', 'original_request')
        .prefetch_related('items__hardware', 'items__service', 'approvals__approval_step'),
        id=quotation_id
    )
    
    # Get workflow status - 5 step approval process
    workflow_steps = [
        {
            'name': 'Sales Staff Review',
            'approved': quotation.sales_staff_approved,
            'date': quotation.sales_staff_review_date,
            'icon': 'fa-user',
            'description': 'Sales staff (creator) reviews and submits quotation',
            'step': 'sales_staff'
        },
        {
            'name': 'Sales Manager Review',
            'approved': quotation.sales_manager_approved,
            'date': quotation.sales_manager_review_date,
            'icon': 'fa-user-tie',
            'description': 'Sales manager reviews quotation accuracy and pricing',
            'step': 'sales_manager'
        },
        {
            'name': 'Technical Review',
            'approved': quotation.technical_feasibility_approved,
            'date': quotation.technical_review_date,
            'icon': 'fa-cogs',
            'description': 'Technical manager verifies feasibility and specifications',
            'step': 'technical'
        },
        {
            'name': 'Financial Review',
            'approved': quotation.financial_approved,
            'date': quotation.financial_review_date,
            'icon': 'fa-dollar-sign',
            'description': 'Financial manager audits profit margins and sustainability',
            'step': 'financial'
        },
        {
            'name': 'Final Approval',
            'approved': quotation.general_manager_approved,
            'date': quotation.final_approval_date,
            'icon': 'fa-check-circle',
            'description': 'General manager provides final approval or rejection',
            'step': 'final'
        }
    ]
    
    return render(request, 'quotations/quotation_detail.html', {
        'quotation': quotation,
        'workflow_steps': workflow_steps,
    })


@login_required
def quotation_create(request, request_id=None):
    customer_request = None
    if request_id:
        customer_request = get_object_or_404(CustomerQuotationRequest, id=request_id)
    
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            quotation = form.save(commit=False)
            quotation.created_by = request.user
            
            # Link to customer request if provided
            if customer_request:
                quotation.original_request = customer_request
                if customer_request.existing_customer:
                    quotation.customer = customer_request.existing_customer
                else:
                    # Create new customer from request data
                    customer = Customer.objects.create(
                        company_name=customer_request.company_name,
                        contact_person=customer_request.contact_person,
                        email=customer_request.email,
                        phone=customer_request.phone,
                        address='',
                        city='Singapore',
                        state='Singapore',
                        postal_code='',
                        country='Singapore'
                    )
                    quotation.customer = customer
                    customer_request.existing_customer = customer
                    customer_request.save()
            
            quotation.save()
            
            # Update customer request status
            if customer_request:
                customer_request.status = 'converted'
                customer_request.converted_quotation = quotation
                customer_request.save()
            
            messages.success(request, f'Quotation {quotation.quotation_number} created successfully!')
            return redirect('quotations:quotation_detail', quotation_id=quotation.id)
    else:
        # Pre-populate form from customer request
        initial_data = {}
        if customer_request:
            initial_data = {
                'title': customer_request.project_title,
                'description': f"{customer_request.project_description}\n\nOriginal Request:\n{customer_request.wishlist_items}",
                'valid_until': customer_request.expected_delivery_date,
            }
        form = QuotationForm(initial=initial_data)
    
    return render(request, 'quotations/quotation_form.html', {
        'form': form,
        'customer_request': customer_request,
    })


@login_required
@require_http_methods(["POST"])
def approve_quotation_step(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id)
    action = request.POST.get('action')
    comments = request.POST.get('comments', '')
    step = request.POST.get('step')
    
    # Check user permissions and update appropriate step
    user_groups = [group.name for group in request.user.groups.all()]
    
    # Step 1: Sales Staff (creator) approval
    if step == 'sales_staff' and 'Sales Staff' in user_groups and quotation.created_by == request.user:
        if action == 'approve':
            quotation.sales_staff_approved = True
            quotation.sales_staff_review_date = timezone.now()
            messages.success(request, 'Sales staff approval completed.')
        elif action == 'reject':
            quotation.status = 'rejected'
            messages.success(request, 'Quotation rejected by sales staff.')
    
    # Step 2: Sales Manager approval
    elif step == 'sales_manager' and 'Sales Manager' in user_groups:
        if action == 'approve':
            quotation.sales_manager_approved = True
            quotation.sales_manager_review_date = timezone.now()
            messages.success(request, 'Sales manager approval completed.')
        elif action == 'reject':
            quotation.status = 'rejected'
            messages.success(request, 'Quotation rejected by sales manager.')
    
    # Step 3: Technical Manager approval
    elif step == 'technical' and 'Technical Manager' in user_groups:
        if action == 'approve':
            quotation.technical_feasibility_approved = True
            quotation.technical_review_date = timezone.now()
            messages.success(request, 'Technical feasibility approval completed.')
        elif action == 'reject':
            quotation.status = 'rejected'
            messages.success(request, 'Quotation rejected at technical review.')
    
    # Step 4: Financial Manager approval
    elif step == 'financial' and 'Financial Manager' in user_groups:
        if action == 'approve':
            quotation.financial_approved = True
            quotation.financial_review_date = timezone.now()
            messages.success(request, 'Financial approval completed.')
        elif action == 'reject':
            quotation.status = 'rejected'
            messages.success(request, 'Quotation rejected at financial review.')
    
    # Step 5: General Manager final approval
    elif step == 'final' and 'General Manager' in user_groups:
        if action == 'approve':
            quotation.general_manager_approved = True
            quotation.final_approval_date = timezone.now()
            quotation.status = 'approved'
            messages.success(request, 'Quotation fully approved by General Manager!')
        elif action == 'reject':
            quotation.status = 'rejected'
            messages.success(request, 'Quotation rejected by General Manager.')
    
    # Legacy support for old 'sales' step (map to sales_manager)
    elif step == 'sales' and 'Sales Manager' in user_groups:
        if action == 'approve':
            quotation.sales_manager_approved = True
            quotation.sales_manager_review_date = timezone.now()
            messages.success(request, 'Sales manager approval completed.')
        elif action == 'reject':
            quotation.status = 'rejected'
            messages.success(request, 'Quotation rejected by sales manager.')
    
    else:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('quotations:quotation_detail', quotation_id=quotation_id)
    
    quotation.save()
    
    # Check if all approvals are complete (5-step process)
    if (quotation.sales_staff_approved and 
        quotation.sales_manager_approved and
        quotation.technical_feasibility_approved and 
        quotation.financial_approved and 
        quotation.general_manager_approved and
        quotation.status != 'rejected'):
        quotation.status = 'approved'
        quotation.save()
    
    return redirect('quotations:quotation_detail', quotation_id=quotation_id)


@login_required
def calculate_quotation_total(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id)
    quotation.calculate_totals()
    
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse({
            'subtotal': str(quotation.subtotal),
            'discount_amount': str(quotation.discount_amount),
            'tax_amount': str(quotation.tax_amount),
            'total_amount': str(quotation.total_amount)
        })
    
    messages.success(request, 'Quotation totals have been recalculated.')
    return redirect('quotations:quotation_detail', quotation_id=quotation_id)


@login_required
@require_http_methods(["POST"])
def assign_request(request, request_id):
    customer_request = get_object_or_404(CustomerQuotationRequest, id=request_id)
    
    if request.user.groups.filter(name__in=['Sales Supervisor', 'General Manager']).exists():
        staff_id = request.POST.get('staff_id')
        if staff_id:
            staff_user = get_object_or_404(User, id=staff_id)
            customer_request.assigned_sales_staff = staff_user
            customer_request.status = 'under_review'
            customer_request.save()
            
            messages.success(request, f'Request assigned to {staff_user.get_full_name() or staff_user.username}')
        else:
            messages.error(request, 'Please select a staff member to assign.')
    else:
        messages.error(request, 'You do not have permission to assign requests.')
    
    return redirect('quotations:request_detail', request_id=request_id)


@login_required
def get_hardware_components(request):
    """API endpoint to get hardware components by category"""
    category = request.GET.get('category', '')
    
    if not category:
        return JsonResponse({'error': 'Category parameter is required'}, status=400)
    
    components = Hardware.objects.filter(
        category=category,
        is_active=True
    ).order_by('brand', 'model')
    
    data = []
    for component in components:
        data.append({
            'id': component.id,
            'name': component.name,
            'brand': component.brand,
            'model': component.model,
            'specs': component.description,
            'price': float(component.unit_price),
            'category': component.category,
            'part_number': component.part_number,
            'processor_specs': component.processor_specs,
            'memory_specs': component.memory_specs,
            'storage_specs': component.storage_specs,
            'network_specs': component.network_specs,
            'power_specs': component.power_specs,
            'display_specs': component.display_specs,
        })
    
    return JsonResponse({'components': data})


@login_required
@require_http_methods(["POST"])
def add_quotation_items(request, quotation_id):
    """API endpoint to add items to a quotation"""
    try:
        quotation = get_object_or_404(Quotation, id=quotation_id)
        
        # Check if user can edit this quotation
        if quotation.status != 'draft':
            return JsonResponse({'error': 'Cannot add items to a quotation that is not in draft status'}, status=403)
        
        data = json.loads(request.body)
        items = data.get('items', [])
        
        # Enhanced logging
        print(f"\n=== ADD QUOTATION ITEMS DEBUG ===")
        print(f"Quotation: {quotation.quotation_number}")
        print(f"Items received: {len(items)}")
        for i, item in enumerate(items):
            print(f"Item {i+1}: ID={item.get('id')}, Qty={item.get('quantity')}, Desc={item.get('description', '')[:50]}")
        
        if not items:
            return JsonResponse({'error': 'No items provided'}, status=400)
        
        added_items = []
        failed_items = []
        
        for item_data in items:
            try:
                # Get the hardware component
                hardware = Hardware.objects.get(id=item_data['id'])
                
                # Always create new quotation item (allow duplicates)
                quotation_item = QuotationItem.objects.create(
                    quotation=quotation,
                    hardware=hardware,
                    item_type='hardware',
                    quantity=item_data.get('quantity', 1),
                    unit_price=hardware.unit_price,
                    description=item_data.get('description', ''),
                    discount_percentage=0,
                )
                
                added_items.append({
                    'id': quotation_item.id,
                    'name': hardware.name,
                    'quantity': quotation_item.quantity,
                    'unit_price': float(quotation_item.unit_price),
                    'total_price': float(quotation_item.total_price),
                })
                
            except Hardware.DoesNotExist:
                # Log the missing hardware component for debugging
                error_msg = f"Hardware component with ID {item_data['id']} not found"
                print(f"ERROR: {error_msg}")
                failed_items.append({'id': item_data['id'], 'error': error_msg})
                continue
            except Exception as e:
                error_msg = f"Error processing item {item_data['id']}: {str(e)}"
                print(f"ERROR: {error_msg}")
                failed_items.append({'id': item_data['id'], 'error': error_msg})
                continue
        
        # Recalculate quotation totals
        quotation.calculate_totals()
        
        # Final logging
        print(f"Items successfully added: {len(added_items)}")
        print(f"Items failed: {len(failed_items)}")
        if failed_items:
            print(f"Failed items: {failed_items}")
        print("=== END DEBUG ===\n")
        
        return JsonResponse({
            'success': True,
            'message': f'Added {len(added_items)} items to quotation',
            'items': added_items,
            'quotation_total': float(quotation.total_amount),
            'items_requested': len(items),
            'items_processed': len(added_items),
            'failed_items': failed_items
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["DELETE"])
def remove_quotation_item(request, quotation_id, item_id):
    """API endpoint to remove an item from a quotation"""
    quotation = get_object_or_404(Quotation, id=quotation_id)
    
    # Check if user can edit this quotation
    if quotation.status != 'draft':
        return JsonResponse({'error': 'Cannot remove items from a quotation that is not in draft status'}, status=403)
    
    try:
        quotation_item = QuotationItem.objects.get(id=item_id, quotation=quotation)
        quotation_item.delete()
        
        # Recalculate quotation totals
        quotation.calculate_totals()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed successfully',
            'quotation_total': float(quotation.total_amount)
        })
        
    except QuotationItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)


@login_required
@require_http_methods(["PUT"])
def update_quotation_item(request, quotation_id, item_id):
    """API endpoint to update a quotation item"""
    quotation = get_object_or_404(Quotation, id=quotation_id)
    
    # Check if user can edit this quotation
    if quotation.status != 'draft':
        return JsonResponse({'error': 'Cannot update items in a quotation that is not in draft status'}, status=403)
    
    try:
        quotation_item = QuotationItem.objects.get(id=item_id, quotation=quotation)
        data = json.loads(request.body)
        
        # Update fields
        if 'quantity' in data:
            quotation_item.quantity = data['quantity']
        if 'unit_price' in data:
            quotation_item.unit_price = data['unit_price']
        if 'discount_percentage' in data:
            quotation_item.discount_percentage = data['discount_percentage']
        if 'description' in data:
            quotation_item.description = data['description']
        
        quotation_item.save()
        
        # Recalculate quotation totals
        quotation.calculate_totals()
        
        return JsonResponse({
            'success': True,
            'message': 'Item updated successfully',
            'item': {
                'id': quotation_item.id,
                'quantity': quotation_item.quantity,
                'unit_price': float(quotation_item.unit_price),
                'total_price': float(quotation_item.total_price),
                'discount_percentage': float(quotation_item.discount_percentage),
            },
            'quotation_total': float(quotation.total_amount)
        })
        
    except QuotationItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)


@login_required
@require_http_methods(["POST"])
def submit_for_approval(request, quotation_id):
    """Submit quotation for approval"""
    quotation = get_object_or_404(Quotation, id=quotation_id)
    
    # Check if user can submit this quotation
    if quotation.status != 'draft':
        return JsonResponse({'error': 'Only draft quotations can be submitted for approval'}, status=403)
    
    # Check if quotation has items
    if not quotation.items.exists():
        return JsonResponse({'error': 'Cannot submit quotation without items'}, status=400)
    
    # Update quotation status and set appropriate approvals based on creator role
    quotation.status = 'pending_approval'
    current_time = timezone.now()
    
    # Check creator's role to determine which steps to auto-approve
    creator_groups = [group.name for group in request.user.groups.all()]
    
    if 'Sales Manager' in creator_groups:
        # Sales Manager created quotation - auto-approve both Sales Staff and Sales Manager steps
        quotation.sales_staff_approved = True
        quotation.sales_staff_review_date = current_time
        quotation.sales_manager_approved = True
        quotation.sales_manager_review_date = current_time
    elif 'Sales Staff' in creator_groups:
        # Sales Staff created quotation - auto-approve Sales Staff step only
        quotation.sales_staff_approved = True
        quotation.sales_staff_review_date = current_time
    # For other roles, just set to pending without auto-approvals
    
    quotation.save()
    
    messages.success(request, f'Quotation {quotation.quotation_number} has been submitted for approval.')
    
    return JsonResponse({
        'success': True,
        'message': 'Quotation submitted for approval successfully',
        'status': quotation.get_status_display()
    })

@login_required
def personnel_cost_estimation(request, quotation_id):
    """View for technical manager to estimate personnel costs"""
    quotation = get_object_or_404(Quotation, id=quotation_id)
    
    # Check if user is technical manager
    if not request.user.groups.filter(name='Technical Manager').exists():
        messages.error(request, 'Only Technical Managers can estimate personnel costs.')
        return redirect('quotations:quotation_detail', quotation_id=quotation_id)
    
    # Get existing personnel costs
    personnel_costs = QuotationPersonnelCost.objects.filter(quotation=quotation)
    
    # Get available cost categories
    cost_categories = PersonnelCostCategory.objects.filter(is_active=True)
    
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        estimated_hours = request.POST.get('estimated_hours')
        hourly_rate = request.POST.get('hourly_rate')
        description = request.POST.get('description')
        complexity_notes = request.POST.get('complexity_notes')
        risk_factors = request.POST.get('risk_factors')
        
        try:
            category = PersonnelCostCategory.objects.get(id=category_id)
            
            # Create or update personnel cost
            personnel_cost, created = QuotationPersonnelCost.objects.get_or_create(
                quotation=quotation,
                cost_category=category,
                defaults={
                    'estimated_hours': estimated_hours,
                    'hourly_rate': hourly_rate,
                    'description': description,
                    'complexity_notes': complexity_notes,
                    'risk_factors': risk_factors,
                    'estimated_by': request.user
                }
            )
            
            if not created:
                # Update existing
                personnel_cost.estimated_hours = estimated_hours
                personnel_cost.hourly_rate = hourly_rate
                personnel_cost.description = description
                personnel_cost.complexity_notes = complexity_notes
                personnel_cost.risk_factors = risk_factors
                personnel_cost.save()
            
            messages.success(request, f'Personnel cost estimation for {category.name} has been saved.')
            
        except PersonnelCostCategory.DoesNotExist:
            messages.error(request, 'Invalid cost category selected.')
        except Exception as e:
            messages.error(request, f'Error saving personnel cost: {str(e)}')
        
        return redirect('quotations:personnel_cost_estimation', quotation_id=quotation_id)
    
    return render(request, 'quotations/personnel_cost_estimation.html', {
        'quotation': quotation,
        'personnel_costs': personnel_costs,
        'cost_categories': cost_categories,
    })


@login_required
@require_http_methods(["POST"])
def submit_personnel_costs_for_review(request, quotation_id):
    """Submit all personnel costs for finance review"""
    quotation = get_object_or_404(Quotation, id=quotation_id)
    
    # Check if user is technical manager
    if not request.user.groups.filter(name='Technical Manager').exists():
        return JsonResponse({'error': 'Only Technical Managers can submit personnel costs'}, status=403)
    
    # Submit all draft personnel costs
    personnel_costs = QuotationPersonnelCost.objects.filter(
        quotation=quotation, 
        status='draft'
    )
    
    submitted_count = 0
    for cost in personnel_costs:
        cost.submit_for_review(request.user)
        submitted_count += 1
    
    return JsonResponse({
        'success': True,
        'message': f'Submitted {submitted_count} personnel cost estimations for finance review',
        'submitted_count': submitted_count
    })


@login_required
def margin_analysis_view(request, quotation_id):
    """View for finance manager to analyze margins"""
    quotation = get_object_or_404(Quotation, id=quotation_id)
    
    # Check if user is finance manager
    if not request.user.groups.filter(name='Financial Manager').exists():
        messages.error(request, 'Only Finance Managers can access margin analysis.')
        return redirect('quotations:quotation_detail', quotation_id=quotation_id)
    
    # Get or create margin analysis
    margin_analysis, created = MarginAnalysis.objects.get_or_create(
        quotation=quotation,
        defaults={'analyzed_by': request.user}
    )
    
    # Get personnel costs for review
    personnel_costs = QuotationPersonnelCost.objects.filter(quotation=quotation)
    pending_personnel_costs = personnel_costs.filter(status='submitted')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_analysis':
            # Update margin analysis
            margin_analysis.project_risk_level = request.POST.get('project_risk_level')
            margin_analysis.technical_risk_notes = request.POST.get('technical_risk_notes')
            margin_analysis.market_risk_notes = request.POST.get('market_risk_notes')
            margin_analysis.operational_risk_notes = request.POST.get('operational_risk_notes')
            margin_analysis.sustainability_assessment = request.POST.get('sustainability_assessment')
            margin_analysis.finance_comments = request.POST.get('finance_comments')
            margin_analysis.recommendations = request.POST.get('recommendations')
            margin_analysis.estimated_competitor_price = request.POST.get('estimated_competitor_price') or None
            margin_analysis.price_competitiveness = request.POST.get('price_competitiveness')
            margin_analysis.save()
            
            messages.success(request, 'Margin analysis has been updated.')
            
        elif action == 'approve_personnel_costs':
            # Approve all pending personnel costs
            for cost in pending_personnel_costs:
                cost.approve(request.user, 'Approved via margin analysis')
            messages.success(request, f'Approved {pending_personnel_costs.count()} personnel cost estimations.')
            
        elif action == 'reject_personnel_costs':
            # Reject personnel costs with comments
            rejection_comments = request.POST.get('rejection_comments', 'Rejected via margin analysis')
            for cost in pending_personnel_costs:
                cost.reject(request.user, rejection_comments)
            messages.success(request, f'Rejected {pending_personnel_costs.count()} personnel cost estimations.')
        
        return redirect('quotations:margin_analysis', quotation_id=quotation_id)
    
    return render(request, 'quotations/margin_analysis.html', {
        'quotation': quotation,
        'margin_analysis': margin_analysis,
        'personnel_costs': personnel_costs,
        'pending_personnel_costs': pending_personnel_costs,
    })
