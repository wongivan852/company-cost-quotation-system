from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Customer, Hardware, Service, Quotation, QuotationItem, 
    ApprovalWorkflow, ApprovalStep, QuotationApproval
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'contact_person', 'email', 'phone', 'city', 'country', 'created_at']
    list_filter = ['country', 'city', 'created_at']
    search_fields = ['company_name', 'contact_person', 'email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Hardware)
class HardwareAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'model', 'category', 'unit_price', 'cost_price', 'margin_display', 'is_active']
    list_filter = ['category', 'brand', 'form_factor', 'interface', 'is_active', 'created_at']
    search_fields = ['name', 'brand', 'model', 'description', 'part_number', 'sku']
    readonly_fields = ['created_at', 'updated_at', 'margin_percentage']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'brand', 'model', 'description', 'is_active')
        }),
        ('Identification', {
            'fields': ('part_number', 'sku', 'form_factor', 'interface'),
            'classes': ('collapse',)
        }),
        ('Pricing', {
            'fields': ('unit_price', 'cost_price', 'unit', 'margin_percentage')
        }),
        ('Technical Specifications', {
            'fields': ('processor_specs', 'memory_specs', 'storage_specs', 'network_specs', 'power_specs', 'display_specs'),
            'classes': ('collapse',)
        }),
        ('Physical Specifications', {
            'fields': ('dimensions', 'weight', 'operating_temp'),
            'classes': ('collapse',)
        }),
        ('Connectivity', {
            'fields': ('ethernet_ports', 'usb_ports', 'wifi_standard', 'bluetooth_version'),
            'classes': ('collapse',)
        }),
        ('Support & Lifecycle', {
            'fields': ('warranty_period', 'support_level', 'eol_date', 'replacement_model'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def margin_display(self, obj):
        margin = obj.margin_percentage
        color = 'green' if margin >= 20 else 'orange' if margin >= 10 else 'red'
        return format_html('<span style="color: {};">{:.1f}%</span>', color, margin)
    margin_display.short_description = 'Margin'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'unit_price', 'unit', 'estimated_hours', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 0
    fields = ['item_type', 'hardware', 'service', 'description', 'quantity', 'unit_price', 'discount_percentage', 'total_price']
    readonly_fields = ['total_price']


class QuotationApprovalInline(admin.TabularInline):
    model = QuotationApproval
    extra = 0
    fields = ['approval_step', 'status', 'approver', 'comments', 'approved_at']
    readonly_fields = ['approved_at']


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ['quotation_number', 'customer', 'title', 'status', 'total_amount', 'created_by', 'created_at', 'valid_until']
    list_filter = ['status', 'created_at', 'valid_until', 'created_by']
    search_fields = ['quotation_number', 'customer__company_name', 'title', 'description']
    readonly_fields = ['quotation_number', 'subtotal', 'discount_amount', 'tax_amount', 'total_amount', 'created_at', 'updated_at']
    inlines = [QuotationItemInline, QuotationApprovalInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('quotation_number', 'customer', 'created_by', 'title', 'description', 'status')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'discount_percentage', 'discount_amount', 'tax_percentage', 'tax_amount', 'total_amount')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at', 'valid_until')
        }),
        ('Terms & Conditions', {
            'fields': ('payment_terms', 'delivery_terms', 'warranty_terms', 'notes'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['calculate_totals']
    
    def calculate_totals(self, request, queryset):
        for quotation in queryset:
            quotation.calculate_totals()
        self.message_user(request, f'Totals recalculated for {queryset.count()} quotations.')
    calculate_totals.short_description = 'Recalculate totals for selected quotations'


class ApprovalStepInline(admin.TabularInline):
    model = ApprovalStep
    extra = 0
    fields = ['step_order', 'name', 'approver', 'is_required', 'min_amount', 'max_amount']


@admin.register(ApprovalWorkflow)
class ApprovalWorkflowAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    inlines = [ApprovalStepInline]


@admin.register(ApprovalStep)
class ApprovalStepAdmin(admin.ModelAdmin):
    list_display = ['workflow', 'step_order', 'name', 'approver', 'is_required', 'min_amount', 'max_amount']
    list_filter = ['workflow', 'is_required', 'approver']
    search_fields = ['name', 'workflow__name', 'approver__username']


@admin.register(QuotationApproval)
class QuotationApprovalAdmin(admin.ModelAdmin):
    list_display = ['quotation', 'approval_step', 'status', 'approver', 'approved_at', 'created_at']
    list_filter = ['status', 'approval_step__workflow', 'approver', 'approved_at']
    search_fields = ['quotation__quotation_number', 'approval_step__name', 'approver__username']
    readonly_fields = ['created_at']