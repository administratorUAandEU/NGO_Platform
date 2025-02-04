ClassicEditor
    .create(document.querySelector('#description'), {
        mediaEmbed: {
            previewsInData: true
        },
        ckfinder: {
            uploadUrl: '/upload_image'
        }
    })
    .catch(error => {
        console.error(error);
    });
