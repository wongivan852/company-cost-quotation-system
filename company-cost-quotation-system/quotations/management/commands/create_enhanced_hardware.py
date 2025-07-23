from django.core.management.base import BaseCommand
from quotations.models import Hardware
from decimal import Decimal


class Command(BaseCommand):
    help = 'Create enhanced hardware catalog with detailed computer components'

    def handle(self, *args, **options):
        # Enhanced hardware catalog
        hardware_data = [
            # Mainboards/Motherboards
            {
                'name': 'ASUS ROG Strix X570-E Gaming',
                'category': 'mainboard',
                'brand': 'ASUS',
                'model': 'ROG Strix X570-E Gaming',
                'description': 'ATX AMD X570 chipset motherboard with WiFi 6E and PCIe 4.0',
                'unit_price': Decimal('485.00'),
                'cost_price': Decimal('350.00'),
                'part_number': '90MB1150-M0EAY0',
                'form_factor': 'atx',
                'interface': 'pcie',
                'processor_specs': 'AMD AM4 Socket (3rd/2nd/1st Gen Ryzen)',
                'memory_specs': '4x DDR4-4400, Max 128GB',
                'network_specs': 'Intel 2.5G Ethernet, WiFi 6E',
                'ethernet_ports': 1,
                'usb_ports': 8,
                'wifi_standard': '802.11ax (WiFi 6E)',
                'bluetooth_version': '5.2',
                'warranty_period': '3 years',
            },
            {
                'name': 'MSI MPG B550 Gaming Plus',
                'category': 'mainboard',
                'brand': 'MSI',
                'model': 'MPG B550 Gaming Plus',
                'description': 'ATX AMD B550 chipset motherboard with DDR4 support',
                'unit_price': Decimal('165.00'),
                'cost_price': Decimal('125.00'),
                'part_number': 'B550GAMINGPLUS',
                'form_factor': 'atx',
                'interface': 'pcie',
                'processor_specs': 'AMD AM4 Socket (3rd Gen Ryzen)',
                'memory_specs': '4x DDR4-4400, Max 128GB',
                'network_specs': 'Realtek 8111H Gigabit Ethernet',
                'ethernet_ports': 1,
                'usb_ports': 6,
                'warranty_period': '3 years',
            },

            # CPUs/Processors
            {
                'name': 'AMD Ryzen 9 7950X',
                'category': 'cpu',
                'brand': 'AMD',
                'model': 'Ryzen 9 7950X',
                'description': '16-core, 32-thread desktop processor with 5.7GHz boost clock',
                'unit_price': Decimal('699.00'),
                'cost_price': Decimal('580.00'),
                'part_number': '100-100000514WOF',
                'processor_specs': '16 cores, 32 threads, 4.5GHz base, 5.7GHz boost',
                'power_specs': '170W TDP',
                'warranty_period': '3 years',
            },
            {
                'name': 'Intel Core i7-13700K',
                'category': 'cpu',
                'brand': 'Intel',
                'model': 'Core i7-13700K',
                'description': '16-core (8P+8E) desktop processor with 5.4GHz boost',
                'unit_price': Decimal('419.00'),
                'cost_price': Decimal('335.00'),
                'part_number': 'BX8071313700K',
                'processor_specs': '16 cores (8P+8E), 24 threads, 3.4GHz base, 5.4GHz boost',
                'power_specs': '125W base TDP, 253W turbo',
                'warranty_period': '3 years',
            },
            {
                'name': 'AMD Ryzen 5 7600X',
                'category': 'cpu',
                'brand': 'AMD',
                'model': 'Ryzen 5 7600X',
                'description': '6-core, 12-thread desktop processor with 5.3GHz boost clock',
                'unit_price': Decimal('299.00'),
                'cost_price': Decimal('240.00'),
                'part_number': '100-100000593WOF',
                'processor_specs': '6 cores, 12 threads, 4.7GHz base, 5.3GHz boost',
                'power_specs': '105W TDP',
                'warranty_period': '3 years',
            },

            # RAM/Memory
            {
                'name': 'G.SKILL Trident Z5 RGB 32GB DDR5-6000',
                'category': 'ram',
                'brand': 'G.SKILL',
                'model': 'F5-6000J3038F16GX2-TZ5RK',
                'description': '32GB (2x16GB) DDR5-6000 RGB memory kit',
                'unit_price': Decimal('199.99'),
                'cost_price': Decimal('150.00'),
                'part_number': 'F5-6000J3038F16GX2-TZ5RK',
                'memory_specs': '32GB (2x16GB) DDR5-6000, CL30-38-38-96, 1.35V',
                'warranty_period': 'Lifetime',
            },
            {
                'name': 'Corsair Vengeance LPX 16GB DDR4-3200',
                'category': 'ram',
                'brand': 'Corsair',
                'model': 'CMK16GX4M2B3200C16',
                'description': '16GB (2x8GB) DDR4-3200 low profile memory kit',
                'unit_price': Decimal('54.99'),
                'cost_price': Decimal('42.00'),
                'part_number': 'CMK16GX4M2B3200C16',
                'memory_specs': '16GB (2x8GB) DDR4-3200, CL16-18-18-36, 1.35V',
                'warranty_period': 'Lifetime',
            },
            {
                'name': 'Kingston Fury Beast 64GB DDR4-3200',
                'category': 'ram',
                'brand': 'Kingston',
                'model': 'KF432C16BBK4/64',
                'description': '64GB (4x16GB) DDR4-3200 high capacity memory kit',
                'unit_price': Decimal('189.99'),
                'cost_price': Decimal('145.00'),
                'part_number': 'KF432C16BBK4/64',
                'memory_specs': '64GB (4x16GB) DDR4-3200, CL16-18-18, 1.35V',
                'warranty_period': 'Lifetime',
            },

            # SSDs/Storage
            {
                'name': 'Samsung 990 PRO 2TB NVMe SSD',
                'category': 'ssd',
                'brand': 'Samsung',
                'model': '990 PRO',
                'description': '2TB PCIe 4.0 NVMe M.2 SSD with 7,450 MB/s read speed',
                'unit_price': Decimal('149.99'),
                'cost_price': Decimal('115.00'),
                'part_number': 'MZ-V9P2T0BW',
                'form_factor': 'm2',
                'interface': 'nvme',
                'storage_specs': '2TB, PCIe 4.0 x4, 7450/6900 MB/s (R/W)',
                'warranty_period': '5 years',
            },
            {
                'name': 'Western Digital Black SN850X 1TB',
                'category': 'ssd',
                'brand': 'Western Digital',
                'model': 'WD Black SN850X',
                'description': '1TB PCIe 4.0 NVMe M.2 SSD for gaming and content creation',
                'unit_price': Decimal('79.99'),
                'cost_price': Decimal('62.00'),
                'part_number': 'WDS100T2X0E',
                'form_factor': 'm2',
                'interface': 'nvme',
                'storage_specs': '1TB, PCIe 4.0 x4, 7300/6600 MB/s (R/W)',
                'warranty_period': '5 years',
            },
            {
                'name': 'Crucial MX4 500GB SATA SSD',
                'category': 'ssd',
                'brand': 'Crucial',
                'model': 'MX4 CT500MX500SSD1',
                'description': '500GB 2.5" SATA III solid state drive',
                'unit_price': Decimal('39.99'),
                'cost_price': Decimal('32.00'),
                'part_number': 'CT500MX500SSD1',
                'form_factor': '2_5_inch',
                'interface': 'sata',
                'storage_specs': '500GB, SATA III, 560/510 MB/s (R/W)',
                'warranty_period': '5 years',
            },

            # GPUs/Graphics Cards
            {
                'name': 'NVIDIA GeForce RTX 4090',
                'category': 'gpu',
                'brand': 'NVIDIA',
                'model': 'GeForce RTX 4090',
                'description': 'High-end graphics card with 24GB GDDR6X memory',
                'unit_price': Decimal('1599.99'),
                'cost_price': Decimal('1350.00'),
                'part_number': '900-1G136-2530-000',
                'interface': 'pcie',
                'display_specs': '24GB GDDR6X, 2520 MHz boost clock, 4x DisplayPort 1.4a, 1x HDMI 2.1',
                'power_specs': '450W TBP, 850W recommended PSU',
                'dimensions': '304 x 137 x 61 mm',
                'warranty_period': '3 years',
            },
            {
                'name': 'AMD Radeon RX 7800 XT',
                'category': 'gpu',
                'brand': 'AMD',
                'model': 'Radeon RX 7800 XT',
                'description': 'High-performance graphics card with 16GB GDDR6 memory',
                'unit_price': Decimal('499.99'),
                'cost_price': Decimal('420.00'),
                'part_number': '21308-01-20G',
                'interface': 'pcie',
                'display_specs': '16GB GDDR6, 2430 MHz boost clock, 3x DisplayPort 2.1, 1x HDMI 2.1',
                'power_specs': '263W TBP, 700W recommended PSU',
                'warranty_period': '3 years',
            },

            # Power Supply Units
            {
                'name': 'Corsair RM850x 850W 80+ Gold',
                'category': 'psu',
                'brand': 'Corsair',
                'model': 'RM850x',
                'description': '850W fully modular 80+ Gold certified power supply',
                'unit_price': Decimal('149.99'),
                'cost_price': Decimal('115.00'),
                'part_number': 'CP-9020200-NA',
                'form_factor': 'atx',
                'power_specs': '850W, 80+ Gold (90% efficiency), fully modular',
                'warranty_period': '10 years',
            },
            {
                'name': 'Seasonic Focus GX-750 750W 80+ Gold',
                'category': 'psu',
                'brand': 'Seasonic',
                'model': 'Focus GX-750',
                'description': '750W fully modular 80+ Gold certified power supply',
                'unit_price': Decimal('119.99'),
                'cost_price': Decimal('95.00'),
                'part_number': 'SSR-750FX',
                'form_factor': 'atx',
                'power_specs': '750W, 80+ Gold (87-90% efficiency), fully modular',
                'warranty_period': '10 years',
            },

            # Cooling Systems
            {
                'name': 'Noctua NH-D15 CPU Cooler',
                'category': 'cooling',
                'brand': 'Noctua',
                'model': 'NH-D15',
                'description': 'Dual tower CPU cooler with two 140mm fans',
                'unit_price': Decimal('109.95'),
                'cost_price': Decimal('85.00'),
                'part_number': 'NH-D15',
                'dimensions': '165 x 150 x 161 mm',
                'power_specs': 'Up to 220W TDP cooling capacity',
                'warranty_period': '6 years',
            },
            {
                'name': 'Corsair iCUE H150i Elite LCD',
                'category': 'cooling',
                'brand': 'Corsair',
                'model': 'iCUE H150i Elite LCD',
                'description': '360mm liquid CPU cooler with LCD display',
                'unit_price': Decimal('299.99'),
                'cost_price': Decimal('225.00'),
                'part_number': 'CW-9060062-WW',
                'dimensions': '397 x 120 x 27 mm (radiator)',
                'power_specs': 'Up to 250W TDP cooling capacity',
                'warranty_period': '5 years',
            },

            # Network Equipment
            {
                'name': 'ASUS AX6000 WiFi 6 Router',
                'category': 'router',
                'brand': 'ASUS',
                'model': 'RT-AX88U',
                'description': 'Dual-band WiFi 6 router with 8 Gigabit LAN ports',
                'unit_price': Decimal('349.99'),
                'cost_price': Decimal('265.00'),
                'part_number': 'RT-AX88U',
                'network_specs': 'AX6000 WiFi 6, 8x Gigabit LAN, 2x USB 3.1',
                'ethernet_ports': 8,
                'usb_ports': 2,
                'wifi_standard': '802.11ax (WiFi 6)',
                'dimensions': '300 x 188 x 60 mm',
                'warranty_period': '3 years',
            },

            # Monitors
            {
                'name': 'Dell UltraSharp U2723QE 27" 4K',
                'category': 'monitor',
                'brand': 'Dell',
                'model': 'U2723QE',
                'description': '27" 4K IPS USB-C hub monitor with 90W power delivery',
                'unit_price': Decimal('529.99'),
                'cost_price': Decimal('420.00'),
                'part_number': '210-BDQC',
                'display_specs': '27" IPS, 3840x2160, 60Hz, 400 nits, 99% sRGB',
                'interface': 'usb_c',
                'ethernet_ports': 1,
                'usb_ports': 4,
                'dimensions': '611.6 x 516.2 x 185 mm',
                'warranty_period': '3 years',
            },
            {
                'name': 'LG 27GP850-B 27" 1440p Gaming',
                'category': 'monitor',
                'brand': 'LG',
                'model': '27GP850-B',
                'description': '27" 1440p Nano IPS gaming monitor with 165Hz refresh rate',
                'unit_price': Decimal('296.99'),
                'cost_price': Decimal('235.00'),
                'part_number': '27GP850-B',
                'display_specs': '27" Nano IPS, 2560x1440, 165Hz, 400 nits, 98% DCI-P3',
                'interface': 'displayport',
                'usb_ports': 2,
                'dimensions': '612 x 556 x 260 mm',
                'warranty_period': '1 year',
            }
        ]

        created_count = 0
        for hw_data in hardware_data:
            hardware, created = Hardware.objects.get_or_create(
                name=hw_data['name'],
                brand=hw_data['brand'],
                model=hw_data['model'],
                defaults=hw_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created hardware: {hardware.name}')
            else:
                self.stdout.write(f'Hardware already exists: {hardware.name}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {len(hardware_data)} hardware items. '
                             f'Created {created_count} new items.')
        )