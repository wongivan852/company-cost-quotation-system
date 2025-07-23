from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quotations.models import Customer, Hardware, Service, ApprovalWorkflow, ApprovalStep
from decimal import Decimal


class Command(BaseCommand):
    help = 'Create sample data for the quotation system'

    def handle(self, *args, **options):
        # Create sample customers
        customers_data = [
            {
                'company_name': 'Tech Solutions Pte Ltd',
                'contact_person': 'Sarah Lim',
                'email': 'sarah@techsolutions.com.sg',
                'phone': '+65 6234 5678',
                'address': '123 Business Park',
                'city': 'Singapore',
                'state': 'Singapore',
                'postal_code': '569877',
            },
            {
                'company_name': 'Digital Innovations Corp',
                'contact_person': 'Michael Tan',
                'email': 'michael@digiinnovations.com',
                'phone': '+65 6345 6789',
                'address': '456 Innovation Drive',
                'city': 'Singapore',
                'state': 'Singapore',
                'postal_code': '138632',
            }
        ]

        for customer_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                company_name=customer_data['company_name'],
                defaults=customer_data
            )
            if created:
                self.stdout.write(f'Created customer: {customer.company_name}')

        # Create sample hardware
        hardware_data = [
            {
                'name': 'PowerEdge R750 Server',
                'category': 'server',
                'brand': 'Dell',
                'model': 'PowerEdge R750',
                'description': '2U rack server with dual Intel Xeon processors',
                'unit_price': Decimal('8500.00'),
                'cost_price': Decimal('6800.00'),
            },
            {
                'name': 'Catalyst 9300 Switch',
                'category': 'network',
                'brand': 'Cisco',
                'model': 'Catalyst 9300-48P',
                'description': '48-port managed switch with PoE+',
                'unit_price': Decimal('3200.00'),
                'cost_price': Decimal('2400.00'),
            },
            {
                'name': 'ThinkPad X1 Carbon',
                'category': 'desktop',
                'brand': 'Lenovo',
                'model': 'X1 Carbon Gen 10',
                'description': 'Ultrabook laptop with Intel Core i7',
                'unit_price': Decimal('2800.00'),
                'cost_price': Decimal('2240.00'),
            }
        ]

        for hw_data in hardware_data:
            hardware, created = Hardware.objects.get_or_create(
                name=hw_data['name'],
                defaults=hw_data
            )
            if created:
                self.stdout.write(f'Created hardware: {hardware.name}')

        # Create sample services
        services_data = [
            {
                'name': 'Server Installation & Configuration',
                'category': 'installation',
                'description': 'Professional server installation and initial configuration',
                'unit_price': Decimal('150.00'),
                'estimated_hours': Decimal('8.0'),
            },
            {
                'name': 'Network Infrastructure Setup',
                'category': 'configuration',
                'description': 'Complete network setup including switch configuration',
                'unit_price': Decimal('120.00'),
                'estimated_hours': Decimal('6.0'),
            },
            {
                'name': 'System Administration Training',
                'category': 'training',
                'description': '1-day training session for system administrators',
                'unit_price': Decimal('800.00'),
                'unit': 'day',
                'estimated_hours': Decimal('8.0'),
            }
        ]

        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'Created service: {service.name}')

        # Create sample users for approval workflow
        users_data = [
            {'username': 'sales_manager', 'email': 'sales@company.com', 'first_name': 'Sales', 'last_name': 'Manager'},
            {'username': 'finance_manager', 'email': 'finance@company.com', 'first_name': 'Finance', 'last_name': 'Manager'},
            {'username': 'general_manager', 'email': 'gm@company.com', 'first_name': 'General', 'last_name': 'Manager'},
        ]

        created_users = {}
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            created_users[user_data['username']] = user
            if created:
                self.stdout.write(f'Created user: {user.username}')

        # Create approval workflow
        workflow, created = ApprovalWorkflow.objects.get_or_create(
            name='Standard Quotation Approval',
            defaults={'description': 'Standard 3-step approval process for quotations'}
        )
        
        if created:
            self.stdout.write(f'Created approval workflow: {workflow.name}')

            # Create approval steps
            approval_steps = [
                {
                    'step_order': 1,
                    'name': 'Sales Manager Approval',
                    'approver': created_users['sales_manager'],
                    'max_amount': Decimal('10000.00'),
                },
                {
                    'step_order': 2,
                    'name': 'Finance Manager Approval',
                    'approver': created_users['finance_manager'],
                    'min_amount': Decimal('5000.00'),
                    'max_amount': Decimal('50000.00'),
                },
                {
                    'step_order': 3,
                    'name': 'General Manager Approval',
                    'approver': created_users['general_manager'],
                    'min_amount': Decimal('25000.00'),
                },
            ]

            for step_data in approval_steps:
                step = ApprovalStep.objects.create(
                    workflow=workflow,
                    **step_data
                )
                self.stdout.write(f'Created approval step: {step.name}')

        self.stdout.write(self.style.SUCCESS('Successfully created sample data!'))