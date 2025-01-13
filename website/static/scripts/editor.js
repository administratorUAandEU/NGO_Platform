ClassicEditor
    .create(document.querySelector('#description'), {
        mediaEmbed: {
            previewsInData: true
        }
    })
    .catch(error => {
        console.error(error);
    });
