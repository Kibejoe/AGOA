document.addEventListener('DOMContentLoaded', function () {
    const statusField = document.querySelector('#id_status');
    const commentsRow = document.querySelector('.form-row.field-comments');

    function toggleCommentsField() {
        if (statusField.value === 'rejected') {
            commentsRow.style.display = '';
        } else {
            commentsRow.style.display = 'none';
        }
    }

    if (statusField && commentsRow) {
        toggleCommentsField(); // Initial check
        statusField.addEventListener('change', toggleCommentsField); // On change
    }
});
