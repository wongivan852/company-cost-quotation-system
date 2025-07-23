from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
import csv
import io


class Customer(models.Model):
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default='Singapore')
    tax_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    class Meta:
        ordering = ['company_name']


class Hardware(models.Model):
    CATEGORY_CHOICES = [
        ('server', 'Server'),
        ('storage', 'Storage'),
        ('network', 'Networking'),
        ('security', 'Security'),
        ('desktop', 'Desktop/Laptop'),
        ('peripheral', 'Peripheral'),
        ('software', 'Software License'),
        ('mainboard', 'Mainboard/Motherboard'),
        ('cpu', 'CPU/Processor'),
        ('ram', 'RAM/Memory'),
        ('internal_storage', 'Internal Storage'),
        ('gpu', 'GPU/Graphics Card'),
        ('connectivity', 'Connectivity Component'),
        ('ssd', 'SSD/Storage Drive'),
        ('hdd', 'HDD/Hard Drive'),
        ('psu', 'Power Supply Unit'),
        ('cooling', 'Cooling System'),
        ('case', 'Computer Case'),
        ('monitor', 'Monitor/Display'),
        ('keyboard', 'Keyboard'),
        ('mouse', 'Mouse'),
        ('printer', 'Printer/Scanner'),
        ('ups', 'UPS/Power Backup'),
        ('cable', 'Cables/Connectors'),
        ('router', 'Router/Gateway'),
        ('switch', 'Network Switch'),
        ('wifi', 'WiFi Equipment'),
        ('firewall', 'Firewall/Security'),
        ('other', 'Other'),
    ]

    FORM_FACTOR_CHOICES = [
        ('', 'Not Applicable'),
        ('atx', 'ATX'),
        ('micro_atx', 'Micro-ATX'),
        ('mini_itx', 'Mini-ITX'),
        ('e_atx', 'E-ATX'),
        ('1u', '1U Rack'),
        ('2u', '2U Rack'),
        ('4u', '4U Rack'),
        ('tower', 'Tower'),
        ('desktop', 'Desktop'),
        ('all_in_one', 'All-in-One'),
        ('external', 'External'),
        ('pcie', 'PCIe Card'),
        ('m2', 'M.2'),
        ('2_5_inch', '2.5 inch'),
        ('3_5_inch', '3.5 inch'),
    ]

    INTERFACE_CHOICES = [
        ('', 'Not Applicable'),
        ('usb_2', 'USB 2.0'),
        ('usb_3', 'USB 3.0/3.1'),
        ('usb_c', 'USB-C'),
        ('thunderbolt', 'Thunderbolt'),
        ('ethernet', 'Ethernet RJ45'),
        ('wifi', 'WiFi'),
        ('bluetooth', 'Bluetooth'),
        ('hdmi', 'HDMI'),
        ('displayport', 'DisplayPort'),
        ('vga', 'VGA'),
        ('dvi', 'DVI'),
        ('sata', 'SATA'),
        ('nvme', 'NVMe'),
        ('pcie', 'PCIe'),
        ('sas', 'SAS'),
        ('fiber', 'Fiber Optic'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    unit = models.CharField(max_length=20, default='unit')
    is_active = models.BooleanField(default=True)
    
    # Enhanced specifications
    part_number = models.CharField(max_length=100, blank=True, help_text="Manufacturer part number")
    sku = models.CharField(max_length=100, blank=True, help_text="Internal SKU")
    form_factor = models.CharField(max_length=20, choices=FORM_FACTOR_CHOICES, blank=True)
    interface = models.CharField(max_length=20, choices=INTERFACE_CHOICES, blank=True)
    
    # Technical specifications (flexible fields)
    processor_specs = models.CharField(max_length=200, blank=True, help_text="CPU: Cores, Clock Speed, etc.")
    memory_specs = models.CharField(max_length=200, blank=True, help_text="RAM: Capacity, Type, Speed")
    storage_specs = models.CharField(max_length=200, blank=True, help_text="Storage: Capacity, Type, Speed")
    network_specs = models.CharField(max_length=200, blank=True, help_text="Network: Ports, Speed, Standards")
    power_specs = models.CharField(max_length=200, blank=True, help_text="Power: Wattage, Efficiency, Voltage")
    display_specs = models.CharField(max_length=200, blank=True, help_text="Display: Resolution, Size, Panel Type")
    
    # Physical specifications
    dimensions = models.CharField(max_length=100, blank=True, help_text="W x D x H in mm or inches")
    weight = models.CharField(max_length=50, blank=True, help_text="Weight in kg or lbs")
    operating_temp = models.CharField(max_length=50, blank=True, help_text="Operating temperature range")
    
    # Connectivity
    ethernet_ports = models.PositiveIntegerField(null=True, blank=True, help_text="Number of Ethernet ports")
    usb_ports = models.PositiveIntegerField(null=True, blank=True, help_text="Number of USB ports")
    wifi_standard = models.CharField(max_length=50, blank=True, help_text="WiFi standard (e.g., 802.11ax)")
    bluetooth_version = models.CharField(max_length=20, blank=True, help_text="Bluetooth version")
    
    # Warranty and support
    warranty_period = models.CharField(max_length=50, blank=True, help_text="Warranty period (e.g., 3 years)")
    support_level = models.CharField(max_length=100, blank=True, help_text="Support level included")
    
    # Additional fields
    eol_date = models.DateField(null=True, blank=True, help_text="End of Life date")
    replacement_model = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, 
                                        help_text="Suggested replacement model")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model} - {self.name}"

    @property
    def margin_percentage(self):
        if self.cost_price and self.unit_price and self.cost_price > 0:
            return ((self.unit_price - self.cost_price) / self.cost_price) * 100
        return 0

    class Meta:
        ordering = ['category', 'brand', 'model']


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('installation', 'Installation'),
        ('configuration', 'Configuration'),
        ('training', 'Training'),
        ('support', 'Support'),
        ('consulting', 'Consulting'),
        ('maintenance', 'Maintenance'),
        ('development', 'Development'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    unit = models.CharField(max_length=20, default='hour')
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name']


class CustomerQuotationRequest(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'), 
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('converted', 'Converted to Quotation'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Reference number
    request_number = models.CharField(max_length=20, unique=True, blank=True)
    
    # Customer information (for new customers who may not be in system yet)
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    existing_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True,
                                        help_text="Link to existing customer if found")
    
    # Request details
    project_title = models.CharField(max_length=200)
    project_description = models.TextField(help_text="Detailed project requirements and specifications")
    wishlist_items = models.TextField(help_text="Customer's wishlist of components or services")
    budget_range = models.CharField(max_length=100, blank=True, help_text="Customer's budget expectation")
    expected_delivery_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Internal tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    assigned_sales_staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name='assigned_requests')
    converted_quotation = models.ForeignKey('Quotation', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Internal notes
    sales_notes = models.TextField(blank=True, help_text="Internal notes from sales team")
    
    def save(self, *args, **kwargs):
        if not self.request_number:
            from datetime import datetime
            year = datetime.now().year
            last_request = CustomerQuotationRequest.objects.filter(request_number__startswith=f'REQ{year}').order_by('-request_number').first()
            if last_request:
                last_number = int(last_request.request_number.split('-')[1])
                self.request_number = f'REQ{year}-{last_number + 1:04d}'
            else:
                self.request_number = f'REQ{year}-0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.request_number} - {self.company_name} - {self.project_title}"
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Customer Quotation Request"
        verbose_name_plural = "Customer Quotation Requests"


class HardwareCostImport(models.Model):
    """Model to track hardware cost imports from CSV files"""
    import_date = models.DateTimeField(auto_now_add=True)
    imported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to='hardware_costs/', help_text="CSV file with hardware costs")
    description = models.TextField(blank=True, help_text="Description of this import")
    records_imported = models.PositiveIntegerField(default=0)
    records_updated = models.PositiveIntegerField(default=0)
    errors_log = models.TextField(blank=True, help_text="Import errors and warnings")
    is_active = models.BooleanField(default=True, help_text="Whether this import is currently active")
    
    def __str__(self):
        return f"Hardware Cost Import {self.import_date.strftime('%Y-%m-%d %H:%M')} by {self.imported_by.username}"
    
    class Meta:
        ordering = ['-import_date']
        verbose_name = "Hardware Cost Import"
        verbose_name_plural = "Hardware Cost Imports"


class PersonnelCostCategory(models.Model):
    """Categories for personnel costs"""
    CATEGORY_CHOICES = [
        ('os_setup', 'Device OS Setup & Apps Installation'),
        ('onsite_install', 'Onsite Installation & Configuration'),
        ('onsite_training', 'Onsite Training'),
        ('onsite_maintenance', 'Onsite Maintenance'),
        ('remote_support', 'Remote Support'),
        ('consulting', 'Technical Consulting'),
        ('project_mgmt', 'Project Management'),
        ('other', 'Other Personnel Services'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(help_text="Detailed description of this personnel cost category")
    standard_hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, 
                                             help_text="Standard hourly rate for this category")
    skill_level_required = models.CharField(max_length=50, blank=True, 
                                          help_text="Required skill level (Junior, Senior, Expert)")
    estimated_hours_range = models.CharField(max_length=50, blank=True,
                                           help_text="Typical hours range (e.g., 4-8 hours)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - ${self.standard_hourly_rate}/hour"
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name = "Personnel Cost Category"
        verbose_name_plural = "Personnel Cost Categories"


class Quotation(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('sent', 'Sent to Customer'),
        ('accepted', 'Accepted by Customer'),
        ('expired', 'Expired'),
    ]

    quotation_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='quotations')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quotations')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Link to original customer request
    original_request = models.ForeignKey(CustomerQuotationRequest, on_delete=models.SET_NULL, null=True, blank=True,
                                       help_text="Original customer request that generated this quotation")
    
    # Address fields
    delivery_address = models.TextField(blank=True, help_text="Address for delivery")
    installation_address = models.TextField(blank=True, help_text="Address for installation")
    billing_address = models.TextField(blank=True, help_text="Address for billing")
    
    # Workflow tracking - 5 step approval process:
    # 1. Sales Staff (who created the quotation)
    sales_staff_approved = models.BooleanField(default=False)
    # 2. Sales Manager
    sales_manager_approved = models.BooleanField(default=False)
    # 3. Technical Manager
    technical_feasibility_approved = models.BooleanField(default=False) 
    # 4. Finance Manager
    financial_approved = models.BooleanField(default=False)
    # 5. General Manager
    general_manager_approved = models.BooleanField(default=False)
    
    # Legacy field - keeping for backward compatibility
    sales_supervisor_approved = models.BooleanField(default=False)
    
    # Workflow timestamps
    sales_staff_review_date = models.DateTimeField(null=True, blank=True)
    sales_manager_review_date = models.DateTimeField(null=True, blank=True)
    sales_review_date = models.DateTimeField(null=True, blank=True)  # Legacy
    technical_review_date = models.DateTimeField(null=True, blank=True)
    financial_review_date = models.DateTimeField(null=True, blank=True)
    final_approval_date = models.DateTimeField(null=True, blank=True)
    
    # Pricing
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=7)  # GST in Singapore
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    valid_until = models.DateField()
    
    # Terms and conditions
    payment_terms = models.TextField(default="Net 30 days")
    delivery_terms = models.TextField(blank=True)
    warranty_terms = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.quotation_number:
            from datetime import datetime
            year = datetime.now().year
            last_quote = Quotation.objects.filter(quotation_number__startswith=f'Q{year}').order_by('-quotation_number').first()
            if last_quote:
                last_number = int(last_quote.quotation_number.split('-')[1])
                self.quotation_number = f'Q{year}-{last_number + 1:04d}'
            else:
                self.quotation_number = f'Q{year}-0001'
        super().save(*args, **kwargs)

    def calculate_totals(self):
        self.subtotal = sum(item.total_price for item in self.items.all())
        self.discount_amount = (self.subtotal * self.discount_percentage / 100)
        discounted_amount = self.subtotal - self.discount_amount
        self.tax_amount = (discounted_amount * self.tax_percentage / 100)
        self.total_amount = discounted_amount + self.tax_amount
        self.save()

    @property
    def total_hardware_cost(self):
        """Calculate total hardware cost price"""
        return sum(item.hardware.cost_price * item.quantity for item in self.items.filter(item_type='hardware'))
    
    @property 
    def total_personnel_cost(self):
        """Calculate total personnel cost"""
        return sum(pc.total_cost for pc in self.personnel_costs.all())
    
    @property
    def total_cost_price(self):
        """Calculate total cost price (hardware + personnel)"""
        return self.total_hardware_cost + self.total_personnel_cost
    
    @property
    def margin_amount(self):
        """Calculate margin amount"""
        return self.total_amount - self.total_cost_price
    
    @property
    def margin_percentage(self):
        """Calculate margin percentage"""
        if self.total_cost_price > 0:
            return (self.margin_amount / self.total_cost_price) * 100
        return 0
    
    @property
    def is_margin_acceptable(self):
        """Check if margin meets minimum threshold (configurable)"""
        return self.margin_percentage >= 15  # 15% minimum margin

    def __str__(self):
        return f"{self.quotation_number} - {self.customer.company_name}"

    class Meta:
        ordering = ['-created_at']


class QuotationItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('hardware', 'Hardware'),
        ('service', 'Service'),
    ]

    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    
    # Override fields
    description = models.TextField(blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Order
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Set unit price from related item if not provided
        if not self.unit_price:
            if self.item_type == 'hardware' and self.hardware:
                self.unit_price = self.hardware.unit_price
            elif self.item_type == 'service' and self.service:
                self.unit_price = self.service.unit_price
        
        # Calculate total price
        from decimal import Decimal
        discounted_price = self.unit_price * (1 - Decimal(str(self.discount_percentage)) / 100)
        self.total_price = self.quantity * discounted_price
        
        super().save(*args, **kwargs)

    def get_item_name(self):
        if self.item_type == 'hardware' and self.hardware:
            return str(self.hardware)
        elif self.item_type == 'service' and self.service:
            return str(self.service)
        return "Unknown Item"

    def __str__(self):
        return f"{self.quotation.quotation_number} - {self.get_item_name()}"

    class Meta:
        ordering = ['quotation', 'order']


class ApprovalWorkflow(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ApprovalStep(models.Model):
    workflow = models.ForeignKey(ApprovalWorkflow, on_delete=models.CASCADE, related_name='steps')
    step_order = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    approver = models.ForeignKey(User, on_delete=models.CASCADE)
    is_required = models.BooleanField(default=True)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.workflow.name} - Step {self.step_order}: {self.name}"

    class Meta:
        ordering = ['workflow', 'step_order']
        unique_together = ['workflow', 'step_order']


class QuotationApproval(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('skipped', 'Skipped'),
    ]

    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='approvals')
    approval_step = models.ForeignKey(ApprovalStep, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approver = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField(blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quotation.quotation_number} - {self.approval_step.name} ({self.status})"

    class Meta:
        ordering = ['quotation', 'approval_step__step_order']
        unique_together = ['quotation', 'approval_step']


class QuotationPersonnelCost(models.Model):
    """Personnel costs estimated by technical manager for each quotation"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted to Finance'),
        ('approved', 'Approved by Finance'),
        ('rejected', 'Rejected by Finance'),
        ('revised', 'Needs Revision'),
    ]
    
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='personnel_costs')
    cost_category = models.ForeignKey(PersonnelCostCategory, on_delete=models.CASCADE)
    
    # Technical manager's estimation
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, 
                                        help_text="Hours estimated by technical manager")
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2,
                                    help_text="Hourly rate for this specific task")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    # Details
    description = models.TextField(help_text="Detailed description of work required")
    complexity_notes = models.TextField(blank=True, 
                                      help_text="Notes about complexity factors affecting estimation")
    risk_factors = models.TextField(blank=True,
                                  help_text="Potential risks that could affect cost/time")
    
    # Workflow
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    estimated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estimated_personnel_costs',
                                   help_text="Technical manager who provided the estimation")
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='reviewed_personnel_costs', 
                                  help_text="Finance manager who reviewed this cost")
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_comments = models.TextField(blank=True, help_text="Finance manager's review comments")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Calculate total cost
        self.total_cost = self.estimated_hours * self.hourly_rate
        super().save(*args, **kwargs)
    
    def submit_for_review(self, user):
        """Submit personnel cost estimation to finance manager"""
        self.status = 'submitted'
        self.submitted_at = timezone.now()
        self.save()
    
    def approve(self, user, comments=''):
        """Approve personnel cost (finance manager)"""
        self.status = 'approved'
        self.reviewed_by = user
        self.reviewed_at = timezone.now()
        self.review_comments = comments
        self.save()
    
    def reject(self, user, comments=''):
        """Reject personnel cost (finance manager)"""
        self.status = 'rejected'
        self.reviewed_by = user
        self.reviewed_at = timezone.now()
        self.review_comments = comments
        self.save()
    
    def __str__(self):
        return f"{self.quotation.quotation_number} - {self.cost_category.name} - ${self.total_cost}"
    
    class Meta:
        ordering = ['quotation', 'cost_category']
        verbose_name = "Personnel Cost Estimation"
        verbose_name_plural = "Personnel Cost Estimations"


class MarginAnalysis(models.Model):
    """Detailed margin analysis for finance manager review"""
    RISK_LEVELS = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'), 
        ('high', 'High Risk'),
        ('critical', 'Critical Risk'),
    ]
    
    SUSTAINABILITY_CHOICES = [
        ('sustainable', 'Sustainable'),
        ('marginal', 'Marginal'),
        ('unsustainable', 'Unsustainable'),
    ]
    
    quotation = models.OneToOneField(Quotation, on_delete=models.CASCADE, related_name='margin_analysis')
    
    # Financial analysis
    total_hardware_cost = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    total_personnel_cost = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    gross_margin = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    margin_percentage = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    
    # Risk assessment
    project_risk_level = models.CharField(max_length=10, choices=RISK_LEVELS, default='medium')
    technical_risk_notes = models.TextField(blank=True, 
                                          help_text="Technical risks that could affect costs")
    market_risk_notes = models.TextField(blank=True,
                                       help_text="Market/competitive risks")
    operational_risk_notes = models.TextField(blank=True,
                                            help_text="Operational risks (resources, timeline)")
    
    # Finance manager assessment
    sustainability_assessment = models.CharField(max_length=15, choices=SUSTAINABILITY_CHOICES,
                                                blank=True, help_text="Overall sustainability assessment")
    finance_comments = models.TextField(blank=True, 
                                      help_text="Finance manager's detailed comments")
    recommendations = models.TextField(blank=True,
                                     help_text="Recommendations for improving margin")
    
    # Competitive analysis
    estimated_competitor_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,
                                                   help_text="Estimated competitor pricing")
    price_competitiveness = models.TextField(blank=True,
                                           help_text="Analysis of price competitiveness")
    
    # Approval tracking
    analyzed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='margin_analyses')
    analyzed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Calculate financial metrics
        self.total_hardware_cost = self.quotation.total_hardware_cost
        self.total_personnel_cost = self.quotation.total_personnel_cost
        self.total_cost = self.total_hardware_cost + self.total_personnel_cost
        self.total_revenue = self.quotation.total_amount
        self.gross_margin = self.total_revenue - self.total_cost
        
        if self.total_cost > 0:
            self.margin_percentage = (self.gross_margin / self.total_cost) * 100
        else:
            self.margin_percentage = 0
            
        super().save(*args, **kwargs)
    
    @property
    def is_margin_healthy(self):
        """Check if margin meets company standards"""
        return self.margin_percentage >= 20  # 20% target margin
    
    @property
    def margin_status(self):
        """Get margin status description"""
        if self.margin_percentage >= 25:
            return "Excellent"
        elif self.margin_percentage >= 20:
            return "Good"
        elif self.margin_percentage >= 15:
            return "Acceptable"
        elif self.margin_percentage >= 10:
            return "Marginal"
        else:
            return "Poor"
    
    def __str__(self):
        return f"{self.quotation.quotation_number} - Margin: {self.margin_percentage:.1f}%"
    
    class Meta:
        verbose_name = "Margin Analysis"
        verbose_name_plural = "Margin Analyses"