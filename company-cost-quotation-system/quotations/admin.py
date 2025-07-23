from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Customer, Hardware, Service, Quotation, QuotationItem, 
    ApprovalWorkflow, ApprovalStep, QuotationApproval,
    HardwareCostImport, PersonnelCostCategory, QuotationPersonnelCost, MarginAnalysis
)
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
import csv
import io


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


class QuotationPersonnelCostInline(admin.TabularInline):
    model = QuotationPersonnelCost
    extra = 0
    fields = ['cost_category', 'estimated_hours', 'hourly_rate', 'total_cost', 'status', 'estimated_by']
    readonly_fields = ['total_cost']


class MarginAnalysisInline(admin.StackedInline):
    model = MarginAnalysis
    extra = 0
    readonly_fields = ['total_hardware_cost', 'total_personnel_cost', 'total_cost', 'total_revenue', 'gross_margin', 'margin_percentage']


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ['quotation_number', 'customer', 'title', 'status', 'total_amount', 'margin_percentage_display', 'created_by', 'created_at', 'valid_until']
    list_filter = ['status', 'created_at', 'valid_until', 'created_by']
    search_fields = ['quotation_number', 'customer__company_name', 'title', 'description']
    readonly_fields = ['quotation_number', 'subtotal', 'discount_amount', 'tax_amount', 'total_amount', 
                      'total_hardware_cost', 'total_personnel_cost', 'total_cost_price', 'margin_amount', 'margin_percentage',
                      'created_at', 'updated_at']
    inlines = [QuotationItemInline, QuotationPersonnelCostInline, MarginAnalysisInline, QuotationApprovalInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('quotation_number', 'customer', 'created_by', 'title', 'description', 'status')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'discount_percentage', 'discount_amount', 'tax_percentage', 'tax_amount', 'total_amount')
        }),
        ('Cost Analysis', {
            'fields': ('total_hardware_cost', 'total_personnel_cost', 'total_cost_price', 'margin_amount', 'margin_percentage'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at', 'valid_until')
        }),
        ('Terms & Conditions', {
            'fields': ('payment_terms', 'delivery_terms', 'warranty_terms', 'notes'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['calculate_totals', 'create_margin_analysis']
    
    def create_margin_analysis(self, request, queryset):
        created = 0
        for quotation in queryset:
            analysis, created_new = MarginAnalysis.objects.get_or_create(
                quotation=quotation,
                defaults={'analyzed_by': request.user}
            )
            if created_new:
                created += 1
        self.message_user(request, f'Created margin analysis for {created} quotations.')
    create_margin_analysis.short_description = 'Create margin analysis for selected quotations'
    
    def calculate_totals(self, request, queryset):
        for quotation in queryset:
            quotation.calculate_totals()
        self.message_user(request, f'Totals recalculated for {queryset.count()} quotations.')
    calculate_totals.short_description = 'Recalculate totals for selected quotations'
    
    def margin_percentage_display(self, obj):
        margin = obj.margin_percentage
        if margin >= 25:
            color = 'green'
        elif margin >= 20:
            color = 'blue'
        elif margin >= 15:
            color = 'orange'
        elif margin >= 10:
            color = 'red'
        else:
            color = 'darkred'
        return format_html('<span style="color: {}; font-weight: bold;">{:.1f}%</span>', color, margin)
    margin_percentage_display.short_description = 'Margin %'


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


@admin.register(HardwareCostImport)
class HardwareCostImportAdmin(admin.ModelAdmin):
    list_display = ['import_date', 'imported_by', 'records_imported', 'records_updated', 'is_active']
    list_filter = ['import_date', 'imported_by', 'is_active']
    readonly_fields = ['records_imported', 'records_updated', 'errors_log', 'import_date']
    
    fieldsets = (
        ('Import Information', {
            'fields': ('csv_file', 'description', 'imported_by', 'import_date')
        }),
        ('Results', {
            'fields': ('records_imported', 'records_updated', 'errors_log', 'is_active')
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only on creation
            obj.imported_by = request.user
            obj.save()
            self.process_csv_import(obj)
        else:
            obj.save()
    
    def process_csv_import(self, import_obj):
        """Process the uploaded CSV file and update hardware costs"""
        try:
            csv_file = import_obj.csv_file
            if not csv_file:
                return
            
            # Read CSV file
            file_data = csv_file.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(file_data))
            
            records_imported = 0
            records_updated = 0
            errors = []
            
            with transaction.atomic():
                for row_num, row in enumerate(csv_reader, start=2):
                    try:
                        # Expected columns: name, brand, model, part_number, cost_price, unit_price
                        name = row.get('name', '').strip()
                        brand = row.get('brand', '').strip()
                        model = row.get('model', '').strip()
                        part_number = row.get('part_number', '').strip()
                        
                        if not all([name, brand, model]):
                            errors.append(f"Row {row_num}: Missing required fields (name, brand, model)")
                            continue
                        
                        # Parse prices
                        try:
                            cost_price = float(row.get('cost_price', 0))
                            unit_price = float(row.get('unit_price', 0))
                        except ValueError:
                            errors.append(f"Row {row_num}: Invalid price values")
                            continue
                        
                        # Find or create hardware
                        hardware_qs = Hardware.objects.filter(
                            name=name, brand=brand, model=model
                        )
                        
                        if part_number:
                            hardware_qs = hardware_qs.filter(part_number=part_number)
                        
                        if hardware_qs.exists():
                            # Update existing
                            hardware = hardware_qs.first()
                            hardware.cost_price = cost_price
                            if unit_price > 0:
                                hardware.unit_price = unit_price
                            hardware.save()
                            records_updated += 1
                        else:
                            errors.append(f"Row {row_num}: Hardware not found - {name} {brand} {model}")
                            
                    except Exception as e:
                        errors.append(f"Row {row_num}: Error processing row - {str(e)}")
            
            # Update import record
            import_obj.records_imported = records_imported
            import_obj.records_updated = records_updated
            import_obj.errors_log = '\n'.join(errors) if errors else 'No errors'
            import_obj.save()
            
        except Exception as e:
            import_obj.errors_log = f"Critical error: {str(e)}"
            import_obj.save()


@admin.register(PersonnelCostCategory)
class PersonnelCostCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'standard_hourly_rate', 'skill_level_required', 'is_active']
    list_filter = ['category', 'skill_level_required', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description', 'is_active')
        }),
        ('Pricing & Requirements', {
            'fields': ('standard_hourly_rate', 'skill_level_required', 'estimated_hours_range')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(QuotationPersonnelCost)
class QuotationPersonnelCostAdmin(admin.ModelAdmin):
    list_display = ['quotation', 'cost_category', 'estimated_hours', 'hourly_rate', 'total_cost', 'status', 'estimated_by']
    list_filter = ['status', 'cost_category__category', 'estimated_by', 'reviewed_by']
    search_fields = ['quotation__quotation_number', 'cost_category__name', 'description']
    readonly_fields = ['total_cost', 'created_at', 'updated_at', 'submitted_at', 'reviewed_at']
    
    fieldsets = (
        ('Cost Estimation', {
            'fields': ('quotation', 'cost_category', 'estimated_hours', 'hourly_rate', 'total_cost')
        }),
        ('Details', {
            'fields': ('description', 'complexity_notes', 'risk_factors')
        }),
        ('Workflow', {
            'fields': ('status', 'estimated_by', 'submitted_at', 'reviewed_by', 'reviewed_at', 'review_comments')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['submit_for_review', 'approve_costs', 'reject_costs']
    
    def submit_for_review(self, request, queryset):
        for cost in queryset.filter(status='draft'):
            cost.submit_for_review(request.user)
        self.message_user(request, f'Submitted {queryset.count()} cost estimations for review.')
    submit_for_review.short_description = 'Submit selected costs for finance review'
    
    def approve_costs(self, request, queryset):
        for cost in queryset.filter(status='submitted'):
            cost.approve(request.user)
        self.message_user(request, f'Approved {queryset.count()} cost estimations.')
    approve_costs.short_description = 'Approve selected cost estimations'
    
    def reject_costs(self, request, queryset):
        for cost in queryset.filter(status='submitted'):
            cost.reject(request.user, 'Rejected via admin action')
        self.message_user(request, f'Rejected {queryset.count()} cost estimations.')
    reject_costs.short_description = 'Reject selected cost estimations'


@admin.register(MarginAnalysis)
class MarginAnalysisAdmin(admin.ModelAdmin):
    list_display = ['quotation', 'margin_percentage', 'margin_status', 'sustainability_assessment', 'project_risk_level', 'analyzed_by']
    list_filter = ['sustainability_assessment', 'project_risk_level', 'analyzed_by']
    search_fields = ['quotation__quotation_number']
    readonly_fields = ['total_hardware_cost', 'total_personnel_cost', 'total_cost', 'total_revenue', 'gross_margin', 'margin_percentage', 'analyzed_at', 'updated_at']
    
    fieldsets = (
        ('Financial Analysis', {
            'fields': ('quotation', 'total_hardware_cost', 'total_personnel_cost', 'total_cost', 'total_revenue', 'gross_margin', 'margin_percentage')
        }),
        ('Risk Assessment', {
            'fields': ('project_risk_level', 'technical_risk_notes', 'market_risk_notes', 'operational_risk_notes')
        }),
        ('Finance Assessment', {
            'fields': ('sustainability_assessment', 'finance_comments', 'recommendations')
        }),
        ('Competitive Analysis', {
            'fields': ('estimated_competitor_price', 'price_competitiveness'),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('analyzed_by', 'analyzed_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def margin_status(self, obj):
        status = obj.margin_status
        colors = {
            'Excellent': 'green',
            'Good': 'blue', 
            'Acceptable': 'orange',
            'Marginal': 'red',
            'Poor': 'darkred'
        }
        color = colors.get(status, 'black')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, status)
    margin_status.short_description = 'Margin Status'