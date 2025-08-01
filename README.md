# Company Cost Quotation System

A Django-based web application for managing company cost quotations, hardware components, and personnel costs.

## Features

- Customer quotation request management
- Hardware cost calculations
- Personnel cost tracking
- Quotation approval workflow
- User management system

## Project Structure

- `quotations/` - Main Django application
- `quotation_system/` - Django project settings
- `db.sqlite3` - SQLite database
- `set_sales_manager_password.py` - Script to set sales manager password
- `set_technical_manager_password.py` - Script to set technical manager password

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate virtual environment: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run the server: `python manage.py runserver`

## Database

The project uses SQLite database (`db.sqlite3`) for development. The database includes tables for:
- Customer quotation requests
- Hardware components and costs
- Personnel cost categories
- User management
- Quotation approvals

## Management Scripts

- `set_sales_manager_password.py` - Sets password for sales manager user
- `set_technical_manager_password.py` - Sets password for technical manager user

## License

This project is proprietary software for internal company use.
