from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .models import (
    CustomerQuotationRequest, Hardware, PersonnelCostCategory,
    Quotation, QuotationHardware, QuotationPersonnelCost
)
from .forms import (
    CustomerQuotationRequestForm, QuotationForm,
    QuotationHardwareForm, QuotationPersonnelCostForm
)


def home(request):
    """Home page view"""
    context = {
        'total_requests': CustomerQuotationRequest.objects.count(),
        'pending_requests': CustomerQuotationRequest.objects.filter(status='pending').count(),
        'total_quotations': Quotation.objects.count(),
        'approved_quotations': Quotation.objects.filter(final_approval=True).count(),
    }
    return render(request, 'quotations/home.html', context)


def customer_request_list(request):
    """List all customer quotation requests"""
    requests = CustomerQuotationRequest.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        requests = requests.filter(
            Q(customer_name__icontains=search_query) |
            Q(company_name__icontains=search_query) |
            Q(project_description__icontains=search_query)
        )
    
    # Status filter
    status_filter = request.GET.get('status')
    if status_filter:
        requests = requests.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': CustomerQuotationRequest._meta.get_field('status').choices,
    }
    return render(request, 'quotations/customer_request_list.html', context)


def customer_request_detail(request, pk):
    """Detail view for customer quotation request"""
    customer_request = get_object_or_404(CustomerQuotationRequest, pk=pk)
    quotations = Quotation.objects.filter(customer_request=customer_request)
    
    context = {
        'customer_request': customer_request,
        'quotations': quotations,
    }
    return render(request, 'quotations/customer_request_detail.html', context)


def customer_request_create(request):
    """Create new customer quotation request"""
    if request.method == 'POST':
        form = CustomerQuotationRequestForm(request.POST)
        if form.is_valid():
            customer_request = form.save()
            messages.success(request, 'Customer request created successfully!')
            return redirect('customer_request_detail', pk=customer_request.pk)
    else:
        form = CustomerQuotationRequestForm()
    
    return render(request, 'quotations/customer_request_form.html', {'form': form})


@login_required
def quotation_list(request):
    """List all quotations"""
    quotations = Quotation.objects.select_related('customer_request', 'created_by')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        quotations = quotations.filter(
            Q(quotation_number__icontains=search_query) |
            Q(customer_request__customer_name__icontains=search_query) |
            Q(customer_request__company_name__icontains=search_query)
        )
    
    # Filter by approval status
    approval_filter = request.GET.get('approval')
    if approval_filter == 'pending':
        quotations = quotations.filter(final_approval=False)
    elif approval_filter == 'approved':
        quotations = quotations.filter(final_approval=True)
    
    # Pagination
    paginator = Paginator(quotations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'approval_filter': approval_filter,
    }
    return render(request, 'quotations/quotation_list.html', context)


@login_required
def quotation_detail(request, pk):
    """Detail view for quotation"""
    quotation = get_object_or_404(Quotation, pk=pk)
    hardware_items = quotation.hardware_items.select_related('hardware')
    personnel_costs = quotation.personnel_costs.select_related('category')
    
    context = {
        'quotation': quotation,
        'hardware_items': hardware_items,
        'personnel_costs': personnel_costs,
    }
    return render(request, 'quotations/quotation_detail.html', context)


@login_required
def quotation_create(request, customer_request_id):
    """Create new quotation for a customer request"""
    customer_request = get_object_or_404(CustomerQuotationRequest, pk=customer_request_id)
    
    if request.method == 'POST':
        form = QuotationForm(request.POST)
        if form.is_valid():
            quotation = form.save(commit=False)
            quotation.customer_request = customer_request
            quotation.created_by = request.user
            quotation.save()
            messages.success(request, 'Quotation created successfully!')
            return redirect('quotation_detail', pk=quotation.pk)
    else:
        form = QuotationForm()
    
    context = {
        'form': form,
        'customer_request': customer_request,
    }
    return render(request, 'quotations/quotation_form.html', context)


def hardware_list(request):
    """List all hardware components"""
    hardware = Hardware.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        hardware = hardware.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(manufacturer__icontains=search_query)
        )
    
    # Category filter
    category_filter = request.GET.get('category')
    if category_filter:
        hardware = hardware.filter(category=category_filter)
    
    # Get all categories for filter
    categories = Hardware.objects.values_list('category', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(hardware, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'categories': categories,
    }
    return render(request, 'quotations/hardware_list.html', context)


def hardware_detail(request, pk):
    """Detail view for hardware component"""
    hardware = get_object_or_404(Hardware, pk=pk)
    return render(request, 'quotations/hardware_detail.html', {'hardware': hardware})


# API Views for AJAX requests
@login_required
def api_hardware_search(request):
    """API endpoint for hardware search"""
    query = request.GET.get('q', '')
    hardware_items = Hardware.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        is_active=True
    )[:10]
    
    results = []
    for item in hardware_items:
        results.append({
            'id': item.id,
            'name': item.name,
            'category': item.category,
            'unit_cost': str(item.unit_cost),
            'currency': item.currency,
        })
    
    return JsonResponse({'results': results})


@login_required
def api_personnel_categories(request):
    """API endpoint for personnel cost categories"""
    categories = PersonnelCostCategory.objects.filter(is_active=True)
    
    results = []
    for category in categories:
        results.append({
            'id': category.id,
            'name': category.name,
            'hourly_rate': str(category.hourly_rate),
            'currency': category.currency,
        })
    
    return JsonResponse({'results': results})
