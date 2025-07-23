from django.urls import path
from . import views

app_name = 'quotations'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Customer-facing URLs
    path('request/', views.customer_request, name='customer_request'),
    path('request/<int:request_id>/submitted/', views.request_submitted, name='request_submitted'),
    
    # Internal URLs - Customer Requests
    path('requests/', views.request_list, name='request_list'),
    path('requests/<int:request_id>/', views.request_detail, name='request_detail'),
    path('requests/<int:request_id>/assign/', views.assign_request, name='assign_request'),
    
    # Quotations
    path('quotations/', views.quotation_list, name='quotation_list'),
    path('quotations/<int:quotation_id>/', views.quotation_detail, name='quotation_detail'),
    path('quotations/create/', views.quotation_create, name='quotation_create'),
    path('quotations/create/<int:request_id>/', views.quotation_create, name='quotation_create_from_request'),
    path('quotations/<int:quotation_id>/calculate/', views.calculate_quotation_total, name='calculate_total'),
    
    # Approval workflow
    path('quotations/<int:quotation_id>/approve/', views.approve_quotation_step, name='approve_quotation_step'),
    path('quotations/<int:quotation_id>/submit/', views.submit_for_approval, name='submit_for_approval'),
    
    # API endpoints
    path('api/components/', views.get_hardware_components, name='api_components'),
    path('api/quotations/<int:quotation_id>/items/', views.add_quotation_items, name='api_add_items'),
    path('api/quotations/<int:quotation_id>/items/<int:item_id>/', views.remove_quotation_item, name='api_remove_item'),
    path('api/quotations/<int:quotation_id>/items/<int:item_id>/update/', views.update_quotation_item, name='api_update_item'),
]