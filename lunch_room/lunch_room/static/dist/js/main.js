

$(document).ready(function () {

    $('.select2').select2({
        width: '100%',
        placeholder: 'Wybierz...',
        allowClear: true,
    });

    $('#participants, #order_groups').select2({
        width: '100%',
        placeholder: 'Wybierz...',
        allowClear: true,
        closeOnSelect: false,
    });



    $("#searchInput").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#restaurantTableBody tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    $("#deleteBtn").click(function () {
        const that = $(this)
        const restName = that.data('restaurant_name')
        const restId = that.data('restaurant_id')
        const returnUrl = that.data('return_url');

        Swal.fire({
            title: 'Czy na pewno?',
            text: `Czy chcesz usunąć jadłodajnię ${restName}?`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Tak, usuń',
            cancelButtonText: 'Anuluj'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: '/restaurant-delete/',
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
                    },
                    data: {
                        'restaurant_id': restId
                    },
                    success: function () {
                        window.location.href = returnUrl;
                    },
                    error: function () {
                        Swal.fire(
                            'Błąd!',
                            'Wystąpił problem podczas usuwania jadłodajni.',
                            'error'
                        );
                    }
                });
            }
        });
    });

    // Add new meal field
    $("#addMealBtn").click(function () {
        const newMeal = `
            <div class="meal-entry mb-3">
                <div class="row">
                    <div class="col-md-8">
                        <input type="text" class="form-control" name="meal_name[]" placeholder="Nazwa potrawy" required>
                    </div>
                    <div class="col-md-3">
                        <input type="number" class="form-control" name="meal_price[]" placeholder="Cena" step="0.01" required>
                    </div>
                    <div class="col-md-1">
                        <button type="button" class="btn btn-danger remove-meal">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        $("#mealsContainer").append(newMeal);
    });


    $(document).on('click', '.remove-meal', function () {
        $(this).closest('.meal-entry').remove();
    });


    $("#restaurantForm").submit(function (e) {
        e.preventDefault();

        const returnUrl = $(this).data('return_url');

        const formData = {
            name: $("#name").val(),
            address: $("#address").val(),
            phone: $("#phone").val(),
            meals: []
        };

        $('.meal-entry').each(function () {
            const meal = {
                name: $(this).find('input[name="meal_name[]"]').val(),
                price: $(this).find('input[name="meal_price[]"]').val()
            };
            formData.meals.push(meal);
        });

        $.ajax({
            url: '/restaurant-create/',
            type: 'POST',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                window.location.href = returnUrl;
            },
            error: function () {
                Swal.fire(
                    'Błąd!',
                    'Wystąpił problem podczas zapisywania jadłodajni.',
                    'error'
                );
            }
        });
    });

    // Add new meal
    $('#saveMealBtn').click(function () {
        const restId = $(this).data('restaurant_id')
        const mealData = {
            name: $('#newMealName').val(),
            price: $('#newMealPrice').val(),
            restaurant_id: restId
        };

        $.ajax({
            url: '/meal-create/',
            type: 'POST',
            data: JSON.stringify(mealData),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function () {
                location.reload();
            },
            error: function () {
                Swal.fire('Błąd!', 'Wystąpił problem podczas dodawania potrawy.', 'error');
            }
        });
    });

    // Edit meal
    $('.edit-meal').click(function () {
        const mealId = $(this).data('meal-id');
        const mealName = $(this).data('meal-name');
        const mealPrice = $(this).data('meal-price');

        $('#editMealId').val(mealId);
        $('#editMealName').val(mealName);
        $('#editMealPrice').val(mealPrice);
    });

    // Edit meal
    $('#updateMealBtn').click(function () {
        const mealData = {
            id: $('#editMealId').val(),
            name: $('#editMealName').val(),
            price: $('#editMealPrice').val()
        };

        $.ajax({
            url: '/meal-edit/',
            type: 'POST',
            data: JSON.stringify(mealData),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function () {
                location.reload();
            },
            error: function () {
                Swal.fire('Błąd!', 'Wystąpił problem podczas aktualizacji potrawy.', 'error');
            }
        });
    });

    // Delete meal
    $('.delete-meal').click(function () {
        const mealId = $(this).data('meal-id');
        const mealName = $(this).data('meal-name');

        Swal.fire({
            title: 'Czy na pewno?',
            text: `Czy chcesz usunąć potrawę "${mealName}"?`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Tak, usuń',
            cancelButtonText: 'Anuluj'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: '/meal-delete/',
                    type: 'POST',
                    data: JSON.stringify({meal_id: mealId}),
                    contentType: 'application/json',
                    headers: {
                        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
                    },
                    success: function () {
                        location.reload();
                    },
                    error: function () {
                        Swal.fire('Błąd!', 'Wystąpił problem podczas usuwania potrawy.', 'error');
                    }
                });
            }
        });
    });

    $('#edit-session-form').on('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        formData.append('lunch_session_id', $(this).data('lunch-session-id'));

        $.ajax({
            url: '/lunch_session_edit/',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                Swal.fire({
                    icon: 'success',
                    title: 'Sukces',
                    text: response.message
                }).then(() => {
                    location.reload();
                });
            },
            error: function (xhr) {
                Swal.fire({
                    icon: 'error',
                    title: 'Błąd',
                    text: xhr.responseJSON?.message || 'Wystąpił błąd'
                });
            }
        });
    });


});