from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Customer, Hardware, Service, Quotation, QuotationItem


class CustomerModelTest(TestCase):
    def test_customer_creation(self):
        customer = Customer.objects.create(
            company_name="Test Company",
            contact_person="John Doe",
            email="john@test.com",
            phone="+65 1234 5678",
            address="123 Test Street",
            city="Singapore",
            state="Singapore",
            postal_code="123456",
            country="Singapore"
        )
        self.assertEqual(str(customer), "Test Company")


class HardwareModelTest(TestCase):
    def test_hardware_margin_calculation(self):
        hardware = Hardware.objects.create(
            name="Test Server",
            category="server",
            brand="Dell",
            model="PowerEdge R750",
            description="High-performance server",
            unit_price=Decimal('5000.00'),
            cost_price=Decimal('4000.00')
        )
        self.assertEqual(hardware.margin_percentage, 25.0)


class QuotationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'password')
        self.customer = Customer.objects.create(
            company_name="Test Customer",
            contact_person="Jane Doe",
            email="jane@test.com",
            phone="+65 8765 4321",
            address="456 Customer Street",
            city="Singapore",
            state="Singapore",
            postal_code="654321",
            country="Singapore"
        )
        self.hardware = Hardware.objects.create(
            name="Test Hardware",
            category="server",
            brand="HP",
            model="ProLiant DL380",
            description="Enterprise server",
            unit_price=Decimal('3000.00'),
            cost_price=Decimal('2400.00')
        )

    def test_quotation_number_generation(self):
        quotation = Quotation.objects.create(
            customer=self.customer,
            created_by=self.user,
            title="Test Quotation",
            valid_until="2025-12-31"
        )
        self.assertTrue(quotation.quotation_number.startswith('Q2025-'))

    def test_quotation_total_calculation(self):
        quotation = Quotation.objects.create(
            customer=self.customer,
            created_by=self.user,
            title="Test Quotation",
            valid_until="2025-12-31",
            tax_percentage=Decimal('7.0')
        )
        
        QuotationItem.objects.create(
            quotation=quotation,
            item_type='hardware',
            hardware=self.hardware,
            quantity=Decimal('2'),
            unit_price=Decimal('3000.00')
        )
        
        quotation.calculate_totals()
        self.assertEqual(quotation.subtotal, Decimal('6000.00'))
        self.assertEqual(quotation.tax_amount, Decimal('420.00'))
        self.assertEqual(quotation.total_amount, Decimal('6420.00'))