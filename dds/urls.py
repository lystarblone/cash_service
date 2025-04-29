from django.contrib import admin
from django.urls import path
from . import views

app_name = 'dds'

urlpatterns = [
    path('', views.index, name='index'),
    path('transaction/create/', views.transaction_create, name='transaction_create'),
    path('transaction/edit/<int:pk>/', views.transaction_edit, name='transaction_edit'),
    path('transaction/delete/<int:pk>', views.transaction_delete, name='transaction_delete'),
]