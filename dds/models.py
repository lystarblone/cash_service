from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

# Модель для статусов транзакций
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Модель для типов транзакций
class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Модель для категорий, связанных с типами
class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'type'], name='unique_category_name_type')
        ]

    def __str__(self):
        return self.name

# Модель для подкатегорий, связанных с категориями
class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'category'], name='unique_subcategory_name_category')
        ]

    def __str__(self):
        return self.name

# Модель для транзакций с валидацией
class Transaction(models.Model):
    created_at = models.DateField(auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True)

    def clean(self):
        if self.category.type != self.type:
            raise ValidationError('Категория должна принадлежать выбранному типу')
        if self.subcategory.category != self.category:
            raise ValidationError('Подкатегория должна принадлежать выбранной категории')

    def __str__(self):
        return f"{self.created_at} - {self.amount} RUB"