document.getElementById('id_cover_pic').onchange = (e) => {
    imageField = e.target;
    if(imageField.files && imageField.files[0]) {
        let fileReader = new FileReader();

        fileReader.readAsDataURL(imageField.files[0]);

        fileReader.onload = (e) => {
            let imagePreview = document.getElementById('img-preview');
            imagePreview.setAttribute('src', e.target.result);
        }
    }
}