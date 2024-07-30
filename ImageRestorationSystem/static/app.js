Dropzone.autoDiscover = false;

var myDropzone = new Dropzone("#dropzone", {
    autoProcessQueue: false,
    url: "/upload",
    maxFiles: 1,
    acceptedFiles: "image/*",
    init: function () {
        var submitBtn = document.querySelector("#submitBtn");
        var myDropzone = this;

        submitBtn.addEventListener("click", function () {
            myDropzone.processQueue();
        });

        this.on("success", function (file, response) {
            // Handle success - for example, display the restored image
            var resultHolder = document.getElementById("resultHolder");
            resultHolder.innerHTML = '<img src="' + URL.createObjectURL(file) + '" class="img-fluid">';
        });

        this.on("error", function (file, errorMessage) {
            // Handle error - for example, display an error message
            var errorHolder = document.getElementById("error");
            errorHolder.style.display = 'block';
            errorHolder.textContent = errorMessage;
        });
    }
});
