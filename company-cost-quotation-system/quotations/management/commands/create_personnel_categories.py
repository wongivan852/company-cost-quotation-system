from django.core.management.base import BaseCommand
from django.db import transaction
from quotations.models import PersonnelCostCategory


class Command(BaseCommand):
    help = 'Create initial personnel cost categories'

    def handle(self, *args, **options):
        personnel_categories = [
            {
                'name': 'Device OS Setup & Software Installation',
                'category': 'os_setup',
                'description': 'Installing and configuring operating system, drivers, and essential software applications on devices',
                'standard_hourly_rate': 85.00,
                'skill_level_required': 'Junior-Senior',
                'estimated_hours_range': '2-4 hours per device'
            },
            {
                'name': 'Network Configuration & Setup',
                'category': 'os_setup', 
                'description': 'Configuring network settings, VPN, security policies, and connectivity on devices',
                'standard_hourly_rate': 95.00,
                'skill_level_required': 'Senior',
                'estimated_hours_range': '1-3 hours per device'
            },
            {
                'name': 'Onsite Hardware Installation',
                'category': 'onsite_install',
                'description': 'Physical installation of servers, networking equipment, and workstations at customer premises',
                'standard_hourly_rate': 120.00,
                'skill_level_required': 'Senior',
                'estimated_hours_range': '4-8 hours per visit'
            },
            {
                'name': 'Server Configuration & Deployment', 
                'category': 'onsite_install',
                'description': 'Complete server setup including OS installation, service configuration, and integration',
                'standard_hourly_rate': 140.00,
                'skill_level_required': 'Expert',
                'estimated_hours_range': '8-16 hours per server'
            },
            {
                'name': 'Network Infrastructure Setup',
                'category': 'onsite_install',
                'description': 'Installation and configuration of switches, routers, firewalls, and cabling',
                'standard_hourly_rate': 130.00,
                'skill_level_required': 'Expert',
                'estimated_hours_range': '6-12 hours per site'
            },
            {
                'name': 'User Training - Basic Systems',
                'category': 'onsite_training',
                'description': 'Training end users on basic system operation, software usage, and troubleshooting',
                'standard_hourly_rate': 100.00,
                'skill_level_required': 'Senior',
                'estimated_hours_range': '2-4 hours per session'
            },
            {
                'name': 'Administrator Training - Advanced',
                'category': 'onsite_training', 
                'description': 'Training system administrators on advanced configuration, maintenance, and monitoring',
                'standard_hourly_rate': 150.00,
                'skill_level_required': 'Expert',
                'estimated_hours_range': '4-8 hours per session'
            },
            {
                'name': 'Security Training & Awareness',
                'category': 'onsite_training',
                'description': 'Training staff on security best practices, policies, and incident response procedures',
                'standard_hourly_rate': 120.00,
                'skill_level_required': 'Expert',
                'estimated_hours_range': '2-6 hours per session'
            },
            {
                'name': 'Preventive Maintenance',
                'category': 'onsite_maintenance',
                'description': 'Regular system maintenance, updates, performance optimization, and health checks',
                'standard_hourly_rate': 110.00,
                'skill_level_required': 'Senior',
                'estimated_hours_range': '2-4 hours per visit'
            },
            {
                'name': 'Emergency Support & Troubleshooting',
                'category': 'onsite_maintenance',
                'description': 'Emergency onsite support for critical system failures and complex troubleshooting',
                'standard_hourly_rate': 180.00,
                'skill_level_required': 'Expert',
                'estimated_hours_range': '2-8 hours per incident'
            },
            {
                'name': 'System Upgrades & Migration',
                'category': 'onsite_maintenance',
                'description': 'Upgrading hardware, migrating data, and updating system configurations',
                'standard_hourly_rate': 160.00,
                'skill_level_required': 'Expert', 
                'estimated_hours_range': '4-12 hours per upgrade'
            },
            {
                'name': 'Remote Technical Support',
                'category': 'remote_support',
                'description': 'Remote troubleshooting, configuration changes, and user assistance via remote access',
                'standard_hourly_rate': 75.00,
                'skill_level_required': 'Junior-Senior',
                'estimated_hours_range': '0.5-2 hours per incident'
            },
            {
                'name': 'Technical Consulting',
                'category': 'consulting',
                'description': 'Expert consultation on system architecture, technology selection, and best practices',
                'standard_hourly_rate': 200.00,
                'skill_level_required': 'Expert',
                'estimated_hours_range': '2-8 hours per consultation'
            },
            {
                'name': 'Project Management',
                'category': 'project_mgmt',
                'description': 'Project coordination, timeline management, and stakeholder communication',
                'standard_hourly_rate': 120.00,
                'skill_level_required': 'Senior',
                'estimated_hours_range': '10-20% of project duration'
            }
        ]

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for cat_data in personnel_categories:
                category, created = PersonnelCostCategory.objects.get_or_create(
                    name=cat_data['name'],
                    category=cat_data['category'],
                    defaults={
                        'description': cat_data['description'],
                        'standard_hourly_rate': cat_data['standard_hourly_rate'],
                        'skill_level_required': cat_data['skill_level_required'],
                        'estimated_hours_range': cat_data['estimated_hours_range'],
                        'is_active': True
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Created: {category.name}')
                    )
                else:
                    # Update existing record
                    category.description = cat_data['description']
                    category.standard_hourly_rate = cat_data['standard_hourly_rate']
                    category.skill_level_required = cat_data['skill_level_required']
                    category.estimated_hours_range = cat_data['estimated_hours_range']
                    category.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'Updated: {category.name}')
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {created_count + updated_count} personnel cost categories '
                f'({created_count} created, {updated_count} updated)'
            )
        )