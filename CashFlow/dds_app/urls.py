from django.urls import path
from django.http import JsonResponse
from .views import MainPageView, TransactionCreateView, TransactionUpdateView
from .models import Category, Subcategory


def get_categories(request):
    operation_type_id = request.GET.get('id_operation_type')
    categories = Category.objects.filter(operation_type_id=operation_type_id)
    options = '<option value="">---------</option>'
    for category in categories:
        options += f'<option value="{category.id}">{category.name}</option>'
    print(options)
    return JsonResponse(options, safe=False)

def get_subcategories(request):
    category_id = request.GET.get('id_category')
    subcategories = Subcategory.objects.filter(category_id=category_id)
    options = '<option value="">---------</option>'
    for subcategory in subcategories:
        options += f'<option value="{subcategory.id}">{subcategory.name}</option>'
    return JsonResponse(options, safe=False)

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('transactions/create/', TransactionCreateView.as_view(), name='transaction_add_modal'),
    path('transaction/update/<int:pk>', TransactionUpdateView.as_view(), name='transaction_add_modal'),

    path('api/get_categories/', get_categories, name='get_categories'),
    path('api/get_subcategories/', get_subcategories, name='get_subcategories'),
]