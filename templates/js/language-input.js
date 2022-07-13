$(document).ready(function(){

    $("#btn_upload").click(function(){
        console.log("click")
        var fd = new FormData();
        var files = $('#file')[0].files;

        // Check file selected or not
        if (files.length > 0) {
           fd.append('file', files[0]);

           $.ajax({
              url: '/api/language/upload',
              type: 'POST',
              data: fd,
              contentType: false,
              processData: false,
              success: function(response) {
                 if (response != 0) {
                    console.log("result:");
                    console.log(response);
                    var resultUrl = `http://localhost:5000/language/${response}`
                    console.log(resultUrl)
                    $('#upload_result').html(`Через деякий час результат буде доступним за посиланням <a href="${resultUrl}">${resultUrl}</a>`)
                    $('#upload_result').show();
                 } else {
                    alert('file not uploaded');
                 }
              },
           });
        } else {
           alert("Please select a file.");
        }
    });
});