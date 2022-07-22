$(document).ready(function(){

    $("#btn_upload").click(function(){
        var fd = new FormData();
        var files = $('#file')[0].files;
        var result_file_name = $('#result_file_name').val().trim();
        var number_of_members_to_display = $('#number_of_members_to_display').val().trim();
        var min_message_threshold = $('#min_message_threshold').val().trim();
        // Check file selected or not
        if (files.length > 0) {
           fd.append('file', files[0]);
           fd.append('result_file_name', result_file_name);
           fd.append('processing_params', JSON.stringify({
             'number_of_members_to_display': parseInt(number_of_members_to_display),
             'min_message_threshold': parseInt(min_message_threshold)
           }));

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