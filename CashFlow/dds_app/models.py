from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Status(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='Статус')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name

class OperationType(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='Тип операции')

    class Meta:
        verbose_name = 'Тип операции'
        verbose_name_plural = 'Типы операций'

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='Категория')
    operation_type = models.ForeignKey(
        OperationType, 
        on_delete=models.CASCADE, 
        related_name='categories', 
        verbose_name='Тип операции'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        unique_together = ('operation_type', 'name')

    def __str__(self):
        return f'{self.operation_type.name} - {self.name}'

class Subcategory(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='Подкатегория')
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='subcategories',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        unique_together = ('category', 'name')
        ordering = ('name',)

    def __str__(self):
        return f'{self.category.operation_type.name} - {self.category.name} - {self.name}'

class Transaction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    created_date = models.DateField(default=timezone.now, verbose_name='Дата создания')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус')
    operation_type = models.ForeignKey(OperationType, on_delete=models.CASCADE, verbose_name='Тип операции')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name='Подкатегория')
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, 
        validators=[MinValueValidator(.01)], 
        verbose_name='Сумма (руб)'
    )
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Движение денежных средств'
        verbose_name_plural = 'Движения денежных средств'
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.created_date.strftime('%d.%m.%Y')} | {self.operation_type.name} {self.amount} руб.'
    
    def clean(self):
        if self.subcategory and self.subcategory.category != self.category:
            raise ValidationError('Подкатегория не принадлежит выбранной категории')
        if self.category.operation_type != self.operation_type:
            raise ValidationError('Категория не принадлежит выбранному типу операции')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def local_start_time(self):
        return timezone.localtime(self.start_time)
