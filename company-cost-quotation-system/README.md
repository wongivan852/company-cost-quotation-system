# Quotation Management System

A comprehensive Django-based quotation management system for businesses to create, manage, and approve quotations with multi-step approval workflows.

## Features

### Core Models
- **Customer Management**: Complete customer information with company details
- **Hardware Catalog**: Hardware items with pricing, categories, and margin tracking
- **Service Catalog**: Service offerings with hourly rates and categories
- **Quotation System**: Full quotation management with line items and calculations
- **Multi-step Approval Workflow**: Configurable approval processes with role-based access

### Key Features
- Automatic quotation numbering (Q2025-0001 format)
- Dynamic pricing calculations with discounts and tax
- Margin tracking for hardware items
- Multi-level approval workflow
- Comprehensive Django admin interface
- RESTful API endpoints for quotation operations

## Project Structure

```
quotation_system/
├── quotation_system/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── quotations/                # Main application
│   ├── models.py             # Database models
│   ├── admin.py              # Admin interface
│   ├── views.py              # View functions
│   ├── urls.py               # URL routing
│   └── migrations/           # Database migrations
├── manage.py
├── requirements.txt
└── README.md
```

## Models Overview

### Customer
- Company details, contact information
- Billing address and tax information

### Hardware
- Product catalog with categories (Server, Storage, Networking, etc.)
- Pricing with cost and margin tracking
- Brand and model information

### Service
- Service offerings with categories (Installation, Support, etc.)
- Hourly rates and estimated duration

### Quotation
- Auto-generated quotation numbers
- Customer association and line items
- Pricing calculations with discounts and tax
- Status tracking through approval workflow

### Approval System
- **ApprovalWorkflow**: Configurable approval processes
- **ApprovalStep**: Individual steps with assigned approvers
- **QuotationApproval**: Tracking approval status for each quotation

## Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run development server:
```bash
python manage.py runserver
```

## Usage

### Admin Interface
Access the Django admin at `http://localhost:8000/admin/` to:
- Manage customers, hardware, and services
- Create and configure approval workflows
- View and manage quotations
- Track approval processes

### Quotation Workflow
1. Create customer record
2. Set up hardware/service catalog
3. Configure approval workflow
4. Create quotation with line items
5. Submit for approval
6. Track approval progress
7. Generate final quotation

## Configuration

### Approval Workflows
Create approval workflows with multiple steps:
- Assign approvers to each step
- Set minimum/maximum amount thresholds
- Configure required vs. optional approvals

### Pricing
- Hardware items include cost and selling price with margin calculation
- Services are typically hourly-based
- Quotations support percentage-based discounts
- Tax calculation (default 7% GST for Singapore)

## API Endpoints

- `GET /quotations/` - List all quotations
- `GET /quotations/<id>/` - Quotation details
- `POST /quotations/create/` - Create new quotation
- `POST /quotations/<id>/approve/<approval_id>/` - Approve/reject quotation step
- `POST /quotations/<id>/calculate/` - Recalculate totals

## Development Notes

- Uses Singapore timezone by default
- SQLite database for development (easily configurable for PostgreSQL/MySQL)
- Includes comprehensive admin interface with inline editing
- Models include validation and auto-calculation methods
- Supports both web interface and API access