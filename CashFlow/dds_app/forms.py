from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from django.urls import reverse_lazy

from .models import *


class transactionsFilters(forms.Form):
    date_from = forms.DateField(
        label='Дата от',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
    )

    date_to = forms.DateField(
        label='Дата до',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
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
            'comment',
        ]
        widgets = {
            'created_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'
            ),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'operation_type': forms.Select(
                attrs={'api-url': reverse_lazy('get_categories')}
            ),
            'category': forms.Select(
                attrs={'api-url': reverse_lazy('get_subcategories')}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if getattr(self.user, 'is_authenticated', False):
            self.fields['status'].queryset = Status.objects.filter(owner=self.user)
            self.fields['operation_type'].queryset = OperationType.objects.filter(
                owner=self.user
            )
        else:
            self.fields['status'].queryset = Status.objects.none()
            self.fields['operation_type'].queryset = OperationType.objects.none()
        self.fields['category'].queryset = Category.objects.none()
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        if (
            getattr(self.user, 'is_authenticated', False)
            and 'operation_type' in self.data
        ):
            try:
                operation_type_id = int(self.data.get('operation_type'))
                self.fields['category'].queryset = Category.objects.filter(
                    owner=self.user, operation_type_id=operation_type_id
                )
            except (ValueError, TypeError):
                pass
        elif (
            getattr(self.user, 'is_authenticated', False) and self.instance.pk
        ):  # Редактирование существующей записи
            self.fields[
                'category'
            ].queryset = self.instance.operation_type.categories.filter(owner=self.user)

        if getattr(self.user, 'is_authenticated', False) and 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(
                    category_id=category_id, category__owner=self.user
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.category:
            self.fields[
                'subcategory'
            ].queryset = self.instance.category.subcategories.all()

        # Добавляем CSS-классы для всех полей
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def _post_clean(self):
        if getattr(self.user, 'is_authenticated', False):
            self.instance.owner = self.user
        super()._post_clean()

    def clean(self):
        cleaned_data = super().clean()
        if not getattr(self.user, 'is_authenticated', False):
            raise forms.ValidationError('Пользователь должен быть авторизован.')
        # Проверка соответствия подкатегории и категории
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')

        if subcategory and category and subcategory.category != category:
            raise forms.ValidationError(
                'Выбранная подкатегория не принадлежит этой категории.'
            )
        if cleaned_data.get('status') and cleaned_data['status'].owner != self.user:
            raise forms.ValidationError(
                'Выбранный статус принадлежит другому пользователю.'
            )
        if (
            cleaned_data.get('operation_type')
            and cleaned_data['operation_type'].owner != self.user
        ):
            raise forms.ValidationError(
                'Выбранный тип операции принадлежит другому пользователю.'
            )
        if category and category.owner != self.user:
            raise forms.ValidationError(
                'Выбранная категория принадлежит другому пользователю.'
            )
        if subcategory and subcategory.category.owner != self.user:
            raise forms.ValidationError(
                'Выбранная подкатегория принадлежит другому пользователю.'
            )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.owner = self.user
        if commit:
            instance.save()
        return instance


class StatusForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        self.instance.owner = self.user
        return super().clean()

    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '32'})
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.owner = self.user
        if commit:
            instance.save()
        return instance


class TypesForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        self.instance.owner = self.user
        return super().clean()

    class Meta:
        model = OperationType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '32'})
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.owner = self.user
        if commit:
            instance.save()
        return instance


class CategoryForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        self.instance.owner = self.user
        return super().clean()

    class Meta:
        model = Category
        fields = ['name', 'operation_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '32'}),
            'operation_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.owner = self.user
        if commit:
            instance.save()
        return instance


class SubcategoryForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['category'].queryset = Category.objects.filter(owner=self.user)

    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '32'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
