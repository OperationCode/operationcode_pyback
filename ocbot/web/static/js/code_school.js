'use strict';


(function () {

    $(':checkbox').checkboxpicker().prop('checked', false);


    Array.from(document.querySelectorAll('form')).map(form => {
        form.addEventListener('submit', submitViaAjax);

    });


    let data = new FormData();
    let submitButton = document.getElementById('submitButton');
    let dropZone = document.getElementById('drop-zone');
    let preview = document.querySelector('img');


    let startUpload = function (file_image) {
        let reader = new FileReader();

        reader.onloadend = function () {

            let image = new Image();
            image.src = reader.result;
            image.onload = function () {

                if ((image.width === 200) && (image.height === 200 )) {
                    preview.src = reader.result;
                    //data.append('school_logo', {uri: image.src, type: 'image', name: 'code_school'} );
                    data.append('school_logo', file_image);

                }
                else {
                    alert('Logo must be 200X200 px');
                }
                console.log(data.get('logo'))
            };
        };
        reader.readAsDataURL(file_image);

    };


    dropZone.ondrop = function (ev) {
        ev.preventDefault();
        this.className = 'upload-drop-zone';

        if (ev.dataTransfer.items) {
            // Use DataTransferItemList interface to access the file(s)
            for (let imageIndex = 0; imageIndex < ev.dataTransfer.items.length; imageIndex++) {
                // If dropped items aren't files, reject them
                if ((ev.dataTransfer.items[imageIndex].kind === 'file') &&
                    (ev.dataTransfer.items[imageIndex].type.match('^image/'))) {
                    let file = ev.dataTransfer.items[imageIndex].getAsFile();


                    startUpload(file)
                }
                else {
                    alert('File must be 200px X 200px image');
                    return;
                }
            }
        } else {
            // Use DataTransfer interface to access the file(s)
            for (let imageIndex = 0; imageIndex < ev.dataTransfer.files.length; imageIndex++) {
                if ((ev.dataTransfer.items[imageIndex].kind === 'file') &&
                    (ev.dataTransfer.items[imageIndex].type.match('^image/'))) {
                    let file = ev.dataTransfer.items[imageIndex].getAsFile();

                    startUpload(file)
                }
                else {
                    alert('not an image');
                    return;
                }
            }
        }

    };

    dropZone.ondragover = function () {
        this.className = 'upload-drop-zone drop';
        return false;
    };

    dropZone.ondragleave = function () {
        this.className = 'upload-drop-zone';
        return false;
    };
    function submitViaAjax(e) {
        e.preventDefault();
        const form = e.target;
        console.log('submitted');

        let newForm = new FormData(form);
        newForm.append('school_logo', data.get('school_logo'));
        fetch(form.action, {
            method: form.attributes.method.value,
            body: newForm
        }).then((response) => {
            return response.json();
        }).then((data) => {
            window.location.replace(data['redirect'])
        })
    }

    let dropzoneId = "drop-zone";

    window.addEventListener("dragenter", function (e) {
        if (e.target.id !== dropzoneId) {
            e.preventDefault();
            e.dataTransfer.effectAllowed = "none";
            e.dataTransfer.dropEffect = "none";
        }
    }, false);

    window.addEventListener("dragover", function (e) {
        if (e.target.id !== dropzoneId) {
            e.preventDefault();
            e.dataTransfer.effectAllowed = "none";
            e.dataTransfer.dropEffect = "none";
        }
    });

    window.addEventListener("drop", function (e) {
        if (e.target.id !== dropzoneId) {
            e.preventDefault();
            e.dataTransfer.effectAllowed = "none";
            e.dataTransfer.dropEffect = "none";
        }
    });


})();
