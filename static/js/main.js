document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('task-form');
    const titleInput = document.getElementById('id_title');
    const titleError = document.getElementById('title-error');
    const confirmDelete = document.getElementById('confirmDelete');

    form.addEventListener('submit', function (event) {
        if (titleInput.value.trim() === '') {
            event.preventDefault();
            titleError.classList.remove('hidden');
        } else {
            titleError.classList.add('hidden');
        }
    });
});

