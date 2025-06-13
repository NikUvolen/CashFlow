(function($) {
    $(document).ready(function() {
        // Функция для загрузки категорий
        function loadCategories(operationTypeId, selectedCategoryId) {
            if (operationTypeId) {
                $.ajax({
                    url: '/api/get_categories/',
                    data: { 'operation_type_id': operationTypeId },
                    success: function(data) {
                        $('#id_category').html(data);
                        if (selectedCategoryId) {
                            $('#id_category').val(selectedCategoryId).trigger('change');
                        }
                    }
                });
            } else {
                $('#id_category').html('<option value="">---------</option>');
                $('#id_subcategory').html('<option value="">---------</option>');
            }
        }

        // Функция для загрузки подкатегорий
        function loadSubcategories(categoryId, selectedSubcategoryId) {
            if (categoryId) {
                $.ajax({
                    url: '/api/get_subcategories/',
                    data: { 'category_id': categoryId },
                    success: function(data) {
                        $('#id_subcategory').html(data);
                        if (selectedSubcategoryId) {
                            $('#id_subcategory').val(selectedSubcategoryId);
                        }
                    }
                });
            } else {
                $('#id_subcategory').html('<option value="">---------</option>');
            }
        }

        // Инициализация при загрузке страницы
        var initialOperationType = $('#id_operation_type').val();
        var initialCategory = $('#id_category').val();
        var initialSubcategory = $('#id_subcategory').val();

        if (initialOperationType) {
            loadCategories(initialOperationType, initialCategory);
        }
        if (initialCategory) {
            loadSubcategories(initialCategory, initialSubcategory);
        }

        // Обработчики изменений
        $('#id_operation_type').change(function() {
            loadCategories($(this).val(), null);
        });

        $('#id_category').change(function() {
            loadSubcategories($(this).val(), null);
        });
    });
})(django.jQuery);