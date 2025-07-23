from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


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