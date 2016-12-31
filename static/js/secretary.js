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