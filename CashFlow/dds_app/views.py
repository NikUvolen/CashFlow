from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from .models import *
from .forms import AddTransactionForm
from .filters import TransactionFilter


class TransactionCreateView(BSModalCreateView):
    form_class = AddTransactionForm
    template_name = 'dds_app/add_transaction_modal_form.html'
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
    template_name = 'dds_app/update_transaction_modal_form.html'
    form_class = AddTransactionForm
    success_url = reverse_lazy('main_page')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class MainPageView(View):
    def get_filters(self, GET, queryset):
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
        # for transaction in transactions:
        #     key = str(transaction.operation_type.name)
        #     if key not in context['canvas_data']:
        #         context['canvas_data'][key] = 0
        #     else:
        #         context['canvas_data'][key] += transaction.amount
        # print(context['canvas_data'])

        if request.user.is_authenticated:
            context = self.login_get_context(request)
            return render(request, 'dds_app/main.html', context=context)
        else:
            return render(request, 'dds_app/welcome_page.html')
