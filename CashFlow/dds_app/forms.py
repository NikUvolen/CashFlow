from django import forms
from django.urls import reverse_lazy
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import *


class transactionsFilters(forms.Form):
    date_from = forms.DateField(
        label='Дата от',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        required=False,
    )

    date_to = forms.DateField(
        label='Дата до',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        required=False,
    )
        

class AddTransactionForm(BSModalModelForm):
    class Meta:
        model = Transaction
        fields = [
            'created_date',
            'status',
            'operation_type',
            'category',
            'subcategory',
            'amount',
            'comment'
        ]
        widgets = {
            'created_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'operation_type': forms.Select(attrs={'api-url': reverse_lazy('get_categories')}),
            'category': forms.Select(attrs={'api-url': reverse_lazy('get_subcategories')})
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['status'].queryset = Status.objects.all()
        self.fields['operation_type'].queryset = OperationType.objects.all()
        self.fields['category'].queryset = Category.objects.none()
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        if 'operation_type' in self.data:
            try:
                operation_type_id = int(self.data.get('operation_type'))
                self.fields['category'].queryset = Category.objects.filter(
                    operation_type_id=operation_type_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:  # Для редактирования существующей записи
            self.fields['category'].queryset = self.instance.operation_type.categories.all()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(
                    category_id=category_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.category:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.all()

        # Добавляем CSS-классы для всех полей
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        # Проверка соответствия подкатегории и категории
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        
        if subcategory and category and subcategory.category != category:
            raise forms.ValidationError("Выбранная подкатегория не принадлежит этой категории.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        print(self.user)
        instance.owner = self.user
        if commit:
            instance.save()
        return instance

