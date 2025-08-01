from django import forms
from .models import (
    CustomerQuotationRequest, Quotation,
    QuotationHardware, QuotationPersonnelCost
)


class CustomerQuotationRequestForm(forms.ModelForm):
    class Meta:
        model = CustomerQuotationRequest
        fields = [
            'customer_name', 'customer_email', 'customer_phone',
            'company_name', 'project_description', 'quantity'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'project_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = [
            'quotation_number', 'markup_percentage', 'tax_percentage',
            'notes', 'valid_until'
        ]
        widgets = {
            'quotation_number': forms.TextInput(attrs={'class': 'form-control'}),
            'markup_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tax_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'valid_until': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class QuotationHardwareForm(forms.ModelForm):
    class Meta:
        model = QuotationHardware
        fields = ['hardware', 'quantity', 'unit_cost', 'notes']
        widgets = {
            'hardware': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class QuotationPersonnelCostForm(forms.ModelForm):
    class Meta:
        model = QuotationPersonnelCost
        fields = ['category', 'hours', 'hourly_rate', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
