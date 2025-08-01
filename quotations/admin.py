from django.contrib import admin
from .models import (
    CustomerQuotationRequest, Hardware, PersonnelCostCategory,
    Quotation, QuotationHardware, QuotationPersonnelCost
)


@admin.register(CustomerQuotationRequest)
class CustomerQuotationRequestAdmin(admin.ModelAdmin):
    list_display = ['request_number', 'customer_name', 'company_name', 'status', 'created_date']
    list_filter = ['status', 'created_date']
    search_fields = ['customer_name', 'company_name', 'request_number']
    readonly_fields = ['created_date', 'updated_date']
    ordering = ['-created_date']


@admin.register(Hardware)
class HardwareAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'manufacturer', 'unit_cost', 'currency', 'is_active']
    list_filter = ['category', 'manufacturer', 'is_active', 'currency']
    search_fields = ['name', 'description', 'model_number']
    readonly_fields = ['created_date', 'updated_date']
    ordering = ['category', 'name']


@admin.register(PersonnelCostCategory)
class PersonnelCostCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'hourly_rate', 'currency', 'is_active']
    list_filter = ['is_active', 'currency']
    search_fields = ['name', 'description']
    ordering = ['name']


class QuotationHardwareInline(admin.TabularInline):
    model = QuotationHardware
    extra = 1
    readonly_fields = ['total_cost']


class QuotationPersonnelCostInline(admin.TabularInline):
    model = QuotationPersonnelCost
    extra = 1
    readonly_fields = ['total_cost']


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = [
        'quotation_number', 'customer_request', 'created_by',
        'technical_approval', 'sales_approval', 'final_approval',
        'total_amount', 'created_date'
    ]
    list_filter = [
        'technical_approval', 'sales_approval', 'final_approval',
        'created_date'
    ]
    search_fields = [
        'quotation_number', 'customer_request__customer_name',
        'customer_request__company_name'
    ]
    readonly_fields = [
        'created_date', 'updated_date', 'hardware_total', 'personnel_total',
        'subtotal', 'markup_amount', 'tax_amount', 'total_amount'
    ]
    inlines = [QuotationHardwareInline, QuotationPersonnelCostInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('quotation_number', 'customer_request', 'created_by', 'notes')
        }),
        ('Approval Status', {
            'fields': (
                ('technical_approval', 'technical_approved_by', 'technical_approval_date'),
                ('sales_approval', 'sales_approved_by', 'sales_approval_date'),
                ('final_approval', 'final_approved_by', 'final_approval_date'),
            )
        }),
        ('Pricing', {
            'fields': (
                ('hardware_total', 'personnel_total'),
                ('markup_percentage', 'markup_amount'),
                ('subtotal', 'tax_percentage', 'tax_amount'),
                'total_amount',
                'valid_until'
            )
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)
        })
    )


@admin.register(QuotationHardware)
class QuotationHardwareAdmin(admin.ModelAdmin):
    list_display = ['quotation', 'hardware', 'quantity', 'unit_cost', 'total_cost']
    list_filter = ['quotation__created_date', 'hardware__category']
    search_fields = ['quotation__quotation_number', 'hardware__name']
    readonly_fields = ['total_cost']


@admin.register(QuotationPersonnelCost)
class QuotationPersonnelCostAdmin(admin.ModelAdmin):
    list_display = ['quotation', 'category', 'hours', 'hourly_rate', 'total_cost']
    list_filter = ['quotation__created_date', 'category']
    search_fields = ['quotation__quotation_number', 'category__name']
    readonly_fields = ['total_cost']
