$(document).ready(function(){

    $("#btn_upload").click(function(){
        var fd = new FormData();
        var files = $('#file')[0].files;
        var result_file_name = $('#result_file_name').val().trim();
        // Check file selected or not
        if (files.length > 0) {
           fd.append('file', files[0]);
           fd.append('result_file_name', result_file_name);

           $.ajax({
              url: '/api/most-active-members/upload',
              type: 'POST',
              data: fd,
              contentType: false,
              processData: false,
              success: function(response) {
                 if (response != 0) {
                    console.log("result:");
                    console.log(response);
                    var resultUrl = `http://localhost:5000/most-active-members/${response}`
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