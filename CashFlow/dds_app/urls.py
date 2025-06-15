from django.urls import path
from django.http import JsonResponse
from .views import *
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
    path('transaction/delete/<int:pk>', TransactionDeleteView.as_view(), name='transaction_del_modal'),
    
    path('managing-directories/', ManagingDirectories.as_view(), name='managing_directories'),
    path('managing-directories/create/status', StatusCreateView.as_view(), name='md_status_add_modal'),
    path('managing-directories/update/status/<int:pk>', StatusUpdateView.as_view(), name='md_status_update_modal'),
    path('managing-directories/delete/status/<int:pk>', StatusDeleteView.as_view(), name='md_status_delete_modal'),
    path('managing-directories/create/operation_type', TypeCreateView.as_view(), name='md_type_add_modal'),
    path('managing-directories/update/operation_type/<int:pk>', TypeUpdateView.as_view(), name='md_type_update_modal'),
    path('managing-directories/delete/operation_type/<int:pk>', TypeDeleteView.as_view(), name='md_type_delete_modal'),
    path('managing-directories/create/category', CategoryCreateView.as_view(), name='md_category_add_modal'),
    path('managing-directories/update/category/<int:pk>', CategoryUpdateView.as_view(), name='md_category_update_modal'),
    path('managing-directories/delete/category/<int:pk>', CategoryDeleteView.as_view(), name='md_category_delete_modal'),
    path('managing-directories/create/subcategory', SubcategoryCreateView.as_view(), name='md_subcategory_add_modal'),
    path('managing-directories/update/subcategory/<int:pk>', SubcategoryUpdateView.as_view(), name='md_subcategory_update_modal'),
    path('managing-directories/delete/subcategory/<int:pk>', SubcategoryDeleteView.as_view(), name='md_subcategory_delete_modal'),

    path('api/get_categories/', get_categories, name='get_categories'),
    path('api/get_subcategories/', get_subcategories, name='get_subcategories'),
]