from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from .models import *
from .forms import AddTransactionForm, StatusForm, TypesForm, CategoryForm, SubcategoryForm
from .filters import TransactionFilter


# ---- MAIN PAGE ----
class TransactionCreateView(BSModalCreateView):
    form_class = AddTransactionForm
    template_name = 'dds_app/modals/add_transaction_modal.html'
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('main_page')

    def get_initial(self):
        initial = super().get_initial()
        initial['created_date'] = timezone.now().date()
        return initial
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class TransactionUpdateView(BSModalUpdateView):
    model = Transaction
    template_name = 'dds_app/modals/update_transaction_modal.html'
    form_class = AddTransactionForm
    success_url = reverse_lazy('main_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_pk'] = self.object.pk
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
class TransactionDeleteView(BSModalDeleteView):
    model = Transaction
    template_name = 'dds_app/modals/delete_transaction_modal.html'
    success_message = 'Транзакция успешно удалена'
    success_url = reverse_lazy('main_page')

class MainPageView(View):
    def get_filters(self, GET, queryset):
        """
            Фильтрация
        """

        date_from = GET.get('start_date')
        date_to = GET.get('end_date')
        status = GET.get('status')
        operation_type = GET.get('operation_type')

        if date_from and not date_to:
            queryset = queryset.filter(created_date__range=(date_from))
        elif not date_from and date_from:
            queryset = queryset.filter(created_date__range=(date_from))
        elif date_from and date_to:
            pass

        if status:
            pass

        if operation_type:
            pass

        return queryset

    def login_get_context(self, request):
        transactions = Transaction.objects.select_related(
            'status',
            'operation_type',
            'category',
            'subcategory',
            'subcategory__category',
            'category__operation_type'
        ).filter(owner=request.user).order_by('-pk')
        transactions_filter = TransactionFilter(request.GET, transactions, owner=request.user)
        transactions = transactions_filter.qs

        context = {
            'filter_form': transactions_filter.form,
            'transactions': transactions, 
            'canvas_data': {}
        }

        return context

    def post(self, request):
        addTransactionForm = AddTransactionForm(request.POST, user=request.user)
        if addTransactionForm.is_valid():
            addTransactionForm.save()
        else:
            addTransactionForm = AddTransactionForm(user=request.user)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = self.login_get_context(request)

            # Конфигурация графика с расходами
            operations_types = list(OperationType.objects.all())
            context['transactions'] = context['transactions'].filter(operation_type__in=operations_types)
            chart = {}
            for type in operations_types:
                chart[str(type.name)] = 0
                for transaction in context['transactions']:
                    if transaction.operation_type == type:
                        chart[str(type.name)] += transaction.amount
            chart = {key: value for key, value in chart.items() if value != 0}

            context['chart'] = chart
            return render(request, 'dds_app/main.html', context=context)
        else:
            return render(request, 'dds_app/welcome_page.html')
        

# ---- Managing Directories page ---
class StatusCreateView(BSModalCreateView):
    form_class = StatusForm
    template_name = 'dds_app/modals/add_status_modal.html'
    success_url = reverse_lazy('managing_directories')

class StatusUpdateView(BSModalUpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'dds_app/modals/update_status_modal.html'
    success_url = reverse_lazy('managing_directories')

class StatusDeleteView(BSModalDeleteView):
    model = Status
    template_name = 'dds_app/modals/delete_status_modal.html'
    success_message = 'Статус успешно удалена'
    success_url = reverse_lazy('managing_directories')

class TypeCreateView(BSModalCreateView):
    form_class = TypesForm
    template_name = 'dds_app/modals/add_type_modal.html'
    success_url = reverse_lazy('managing_directories')

class TypeUpdateView(BSModalUpdateView):
    model = OperationType
    form_class = TypesForm
    template_name = 'dds_app/modals/update_type_modal.html'
    success_url = reverse_lazy('managing_directories')

class TypeDeleteView(BSModalDeleteView):
    model = OperationType
    template_name = 'dds_app/modals/delete_type_modal.html'
    success_message = 'Тип успешно удалена'
    success_url = reverse_lazy('managing_directories')

class CategoryCreateView(BSModalCreateView):
    form_class = CategoryForm
    template_name = 'dds_app/modals/add_category_modal.html'
    success_url = reverse_lazy('managing_directories')

class CategoryUpdateView(BSModalUpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dds_app/modals/update_category_modal.html'
    success_url = reverse_lazy('managing_directories')

    def form_valid(self, form):
        transactions = Transaction.objects.filter(category=self.object)
        for transaction in transactions:
            transaction.operation_type = self.object.operation_type
        Transaction.objects.bulk_update(transactions, ['operation_type'])

        response = super().form_valid(form)
        
        return response

class CategoryDeleteView(BSModalDeleteView):
    model = Category
    template_name = 'dds_app/modals/delete_category_modal.html'
    success_message = 'Категория успешно удалена'
    success_url = reverse_lazy('managing_directories')

class SubcategoryCreateView(BSModalCreateView):
    form_class = SubcategoryForm
    template_name = 'dds_app/modals/add_subcategory_modal.html'
    success_url = reverse_lazy('managing_directories')

class SubcategoryUpdateView(BSModalUpdateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'dds_app/modals/update_subcategory_modal.html'
    success_url = reverse_lazy('managing_directories')

    def form_valid(self, form):
        transactions = Transaction.objects.filter(subcategory=self.object)
        for transaction in transactions:
            transaction.category = self.object.category
        Transaction.objects.bulk_update(transactions, ['category'])

        response = super().form_valid(form)
        
        return response

class SubcategoryDeleteView(BSModalDeleteView):
    model = Subcategory
    template_name = 'dds_app/modals/delete_subcategory_modal.html'
    success_message = 'Подкатегория успешно удалена'
    success_url = reverse_lazy('managing_directories')

class ManagingDirectories(View):
    def get(self, request, *args, **kwargs):
        status = Status.objects.all().order_by('-pk')
        operations_types = OperationType.objects.values('pk', 'name').order_by('-pk')
        categories = Category.objects.values('pk', 'name').order_by('-pk')
        subcategories = Subcategory.objects.values('pk', 'name').order_by('-pk')

        context = {
            'status': status,
            'operations_types': operations_types,
            'categories': categories,
            'subcategories': subcategories
        }

        return render(request, 'dds_app/managing_directories.html', context=context)
