from django import forms
from django.contrib.auth.models import User
from .models import CustomerQuotationRequest, Quotation, Customer


class CustomerQuotationRequestForm(forms.ModelForm):
    class Meta:
        model = CustomerQuotationRequest
        fields = [
            'company_name', 'contact_person', 'email', 'phone',
            'project_title', 'project_description', 'wishlist_items',
            'budget_range', 'expected_delivery_date', 'priority'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Company Name'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@company.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+65 1234 5678'
            }),
            'project_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Office Network Infrastructure Upgrade'
            }),
            'project_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Please provide detailed requirements...'
            }),
            'wishlist_items': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'List specific components or services needed...'
            }),
            'budget_range': forms.Select(attrs={
                'class': 'form-select'
            }),
            'expected_delivery_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = [
            'customer', 'title', 'description', 'valid_until',
            'delivery_address', 'installation_address', 'billing_address',
            'discount_percentage', 'tax_percentage',
            'payment_terms', 'delivery_terms', 'warranty_terms', 'notes'
        ]
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'valid_until': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter delivery address...'}),
            'installation_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter installation address...'}),
            'billing_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter billing address...'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'step': '0.01'}),
            'tax_percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'step': '0.01'}),
            'payment_terms': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'delivery_terms': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'warranty_terms': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.all().order_by('company_name')
        self.fields['customer'].empty_label = "Select a customer..."


class AssignStaffForm(forms.Form):
    staff_member = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Sales Staff'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select staff member..."
    )


class ApprovalCommentForm(forms.Form):
    comments = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Add your comments here...'
        }),
        required=False
    )