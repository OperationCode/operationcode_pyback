'use strict';


(function () {

    $(':checkbox').checkboxpicker().prop('checked', false);


    Array.from(document.querySelectorAll('form')).map(form => {
        form.addEventListener('submit', submitViaAjax);

    });

    function submitViaAjax(e) {
        e.preventDefault();
        const form = e.target;


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

    const data = new FormData();
    const submitButton = document.getElementById('submitButton');
    const dropZone = document.getElementById('drop-zone');
    const preview = document.querySelector('img');


    let startUpload = function (file_image) {
        let reader = new FileReader();

        reader.onloadend = () => {
            let image = new Image();
            image.src = reader.result;
            image.onload = function () {


                if ((image.width === 200) && (image.height === 200 )) {
                    preview.src = reader.result;
                    data.append('school_logo', file_image);
                    adjustDropText('', 'hidden');
                }
                else {
                    preview.src = '';

                    adjustDropText('Logo must be 200x200 px and less than 500kb', 'errorClass');
                }
            };
        };
        reader.readAsDataURL(file_image);

    };


    const adjustDropText = (newText, newClass) => {


        let dropTextElement = document.getElementById("drop-text");


        dropTextElement.innerHTML = newText;
        if (newClass === 'hidden') {


            dropTextElement.classList.add('visuallyhidden');
            preview.classList.remove('visuallyhidden');

        }
        else {
            dropTextElement.classList.remove('visuallyhidden');
            preview.classList.add('visuallyhidden');
            dropTextElement.classList.add(newClass);

        }
    };


    dropZone.ondrop = function (ev) {
        ev.preventDefault();
        this.className = 'upload-drop-zone';
        console.log('dropped even handler')
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
                    adjustDropText('Logo must be 200x200 px and less than 500kb', 'errorClass');
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
                    adjustDropText('Logo must be 200x200 px and less than 500kb', 'errorClass');
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

    const dropableDomElements = ['drop-text', 'drop-zone', 'drop-image']

    window.addEventListener("dragenter", function (e) {
        if (!dropableDomElements.includes(e.target.id)) {
            e.preventDefault();
            e.dataTransfer.effectAllowed = "none";
            e.dataTransfer.dropEffect = "none";
        }
    }, false);

    window.addEventListener("dragover", function (e) {
        if (!dropableDomElements.includes(e.target.id)) {
            e.preventDefault();
            e.dataTransfer.effectAllowed = "none";
            e.dataTransfer.dropEffect = "none";
        }
    });

    window.addEventListener("drop", function (e) {
        if (!dropableDomElements.includes(e.target.id)) {
            e.preventDefault();
            e.dataTransfer.effectAllowed = "none";
            e.dataTransfer.dropEffect = "none";
        }
    });


})();
