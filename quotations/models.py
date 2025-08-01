from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class CustomerQuotationRequest(models.Model):
    """Model for customer quotation requests"""
    request_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    project_description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('quoted', 'Quoted'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.customer_name} - {self.project_description[:50]}"


class Hardware(models.Model):
    """Model for hardware components"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    supplier = models.CharField(max_length=200, blank=True)
    lead_time_days = models.PositiveIntegerField(default=0)
    minimum_order_quantity = models.PositiveIntegerField(default=1)
    
    # Additional specifications
    power_consumption = models.CharField(max_length=100, blank=True)
    dimensions = models.CharField(max_length=100, blank=True)
    weight = models.CharField(max_length=50, blank=True)
    operating_temperature = models.CharField(max_length=100, blank=True)
    connectivity_options = models.TextField(blank=True)
    bluetooth_version = models.CharField(max_length=50, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.category})"


class PersonnelCostCategory(models.Model):
    """Model for personnel cost categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Personnel Cost Categories"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.hourly_rate} {self.currency}/hr"


class Quotation(models.Model):
    """Model for quotations"""
    quotation_number = models.CharField(max_length=50, unique=True)
    customer_request = models.ForeignKey(CustomerQuotationRequest, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quotations')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Approval workflow
    technical_approval = models.BooleanField(default=False)
    technical_approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='technical_approvals'
    )
    technical_approval_date = models.DateTimeField(null=True, blank=True)
    
    sales_approval = models.BooleanField(default=False)
    sales_approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sales_approvals'
    )
    sales_approval_date = models.DateTimeField(null=True, blank=True)
    
    final_approval = models.BooleanField(default=False)
    final_approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='final_approvals'
    )
    final_approval_date = models.DateTimeField(null=True, blank=True)
    
    # Pricing
    hardware_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    personnel_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    markup_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    markup_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    notes = models.TextField(blank=True)
    valid_until = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return f"Quote {self.quotation_number} - {self.customer_request.customer_name}"


class QuotationHardware(models.Model):
    """Model for hardware items in a quotation"""
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='hardware_items')
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['quotation', 'hardware']
    
    def save(self, *args, **kwargs):
        self.total_cost = self.unit_cost * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.hardware.name} x {self.quantity}"


class QuotationPersonnelCost(models.Model):
    """Model for personnel costs in a quotation"""
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='personnel_costs')
    category = models.ForeignKey(PersonnelCostCategory, on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['quotation', 'category']
    
    def save(self, *args, **kwargs):
        self.total_cost = self.hours * self.hourly_rate
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.category.name} - {self.hours} hrs"
