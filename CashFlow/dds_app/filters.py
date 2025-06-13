from django import forms
from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from .models import *


class TransactionFilter(FilterSet):
    class Meta:
        model = Transaction
        exclude = ['owner', 'amount', 'comment']

    date_from = DateFilter(
        field_name='created_date',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Дата от'
    )
    
    date_to = DateFilter(
        field_name='created_date',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Дата до'
    )

    status = ModelChoiceFilter(
        field_name='status',
        queryset = Status.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        required=False,
        label='Статус'
    )

    operation_type = ModelChoiceFilter(
        field_name='operation_type',
        queryset = OperationType.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        required=False,
        label='Тип операции'
    )

    category = ModelChoiceFilter(
        field_name='category',
        queryset = Category.objects.none(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        required=False,
        label='Категория'
    )

    subcategory = ModelChoiceFilter(
        field_name='subcategory',
        queryset = Subcategory.objects.none(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        required=False,
        label='Подкатегория'
    )

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)

        if owner:
            self.filters['subcategory'].queryset = Subcategory.objects.values_list('name', flat=True)
            self.filters['category'].queryset = Category.objects.values_list('name', flat=True)
