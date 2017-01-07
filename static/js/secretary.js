function deleteSecretary(secretaryUsername, token) {
    $.ajax({
        method: 'POST',
        url: '/ajax/delete_secretary/',
        data: {
            'username': secretaryUsername,
            'csrfmiddlewaretoken': token
        },
        dataType: 'json',
        success: function () {
            location.reload();
        }
    });
}

function reserveTime(reservationPk, token) {
    $.ajax({
        method: 'POST',
        url: '/ajax/reserve_time/',
        data: {
            'reservationPk': reservationPk,
            'rangeNum': $("#select" + reservationPk + " option:selected").text().trim(),
            'csrfmiddlewaretoken': token
        },
        dataType: 'json',
        success: function () {
            $("#row" + reservationPk).remove()
        }
    });
}