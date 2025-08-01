from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Customer Requests
    path('requests/', views.customer_request_list, name='customer_request_list'),
    path('requests/<int:pk>/', views.customer_request_detail, name='customer_request_detail'),
    path('requests/create/', views.customer_request_create, name='customer_request_create'),
    
    # Quotations
    path('quotations/', views.quotation_list, name='quotation_list'),
    path('quotations/<int:pk>/', views.quotation_detail, name='quotation_detail'),
    path('quotations/create/<int:customer_request_id>/', views.quotation_create, name='quotation_create'),
    
    # Hardware
    path('hardware/', views.hardware_list, name='hardware_list'),
    path('hardware/<int:pk>/', views.hardware_detail, name='hardware_detail'),
    
    # API endpoints
    path('api/hardware/search/', views.api_hardware_search, name='api_hardware_search'),
    path('api/personnel/categories/', views.api_personnel_categories, name='api_personnel_categories'),
]
