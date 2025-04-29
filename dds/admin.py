from django.contrib import admin
from .models import Status, Type, Category, Subcategory, Transaction

# Register your models here.

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['type']

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'status', 'type', 'category', 'subcategory', 'amount']
    list_filter = ['status', 'type', 'category', 'subcategory']