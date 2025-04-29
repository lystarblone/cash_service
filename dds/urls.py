from django.contrib import admin
from django.urls import path
from . import views

app_name = 'dds'

urlpatterns = [
    path('', views.index, name='index'),
    path('transaction/create/', views.transaction_create, name='transaction_create'),
    path('transaction/edit/<int:pk>/', views.transaction_edit, name='transaction_edit'),
    path('transaction/delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),
    path('get-categories/', views.get_categories, name='get_categories'),
    path('get-subcategories/', views.get_subcategories, name='get_subcategories'),
    path('get-statuses/', views.get_statuses, name='get_statuses'),
    path('create-status/', views.create_status, name='create_status'),
    path('get-types/', views.get_types, name='get_types'),
    path('create-type/', views.create_type, name='create_type'),
    path('create-category/', views.create_category, name='create_category'),
    path('create-subcategory/', views.create_subcategory, name='create_subcategory'),
    path('dictionaries/', views.dictionaries, name='dictionaries'),
]