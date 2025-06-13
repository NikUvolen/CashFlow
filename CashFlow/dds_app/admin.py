from django.contrib import admin
from django import forms
from django.urls import reverse_lazy
from .models import *


class TransactionsForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'operation_type': forms.Select(attrs={
                'data-url': reverse_lazy('get_categories')
            }),
            'category': forms.Select(attrs={
                'data-url': reverse_lazy('get_subcategories')
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            if self.instance.operation_type:
                self.fields['category'].queryset = Category.objects.filter(
                    operation_type=self.instance.operation_type
                )
            if self.instance.category:
                self.fields['subcategory'].queryset = Subcategory.objects.filter(
                    category=self.instance.category
                )

@admin.register(OperationType)
class OperationTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'operation_type')
    list_filter = ('operation_type',)
    search_fields = ('name', 'operation_type__name')
    list_select_related = ('operation_type',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'operation_type',)
    list_filter = ('category__operation_type', 'category',)
    search_fields = ('name', 'category__name',)
    list_select_related = ('category', 'category__operation_type',)
    
    def operation_type(self, obj):
        return obj.category.operation_type
    # operation_type.short_descti

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # form = TransactionsForm
    list_display = ('created_date', 'operation_type', 'category', 'subcategory', 'status', 'amount', 'comment_short',)
    list_filter = ('owner', 'status', 'operation_type', 'created_date')
    search_fields = ('owner__username', 'category__name', 'subcategory__name',)
    date_hierarchy = 'created_date'
    list_select_related = ('operation_type', 'category', 'subcategory', 'status',)
    autocomplete_fields = ('category', 'subcategory', 'status',)

    fieldsets = (
        (None, {
            'fields': ('created_date', 'status', 'operation_type', 'amount')
        }),
        ('Категоризация', {
            'fields': ('category', 'subcategory'),
            'classes': ('collapse',)
        }),
        ('Дополнительно', {
            'fields': ('comment',),
            'classes': ('collapse',)
        }),
    )

    # class Media:
    #     js = (
    #         'admin/js/jquery.init.js',
    #         'dds_app/js/transactions_admin.js',  # Кастомный JS для динамических фильтров
    #     )

    def comment_short(self, obj):
        return obj.comment[:50] + '...' if obj.comment else ''
    comment_short.short_description = 'Комментарий'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(owner=request.user)
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner = request.user
        return super().save_model(request, obj, form, change)
