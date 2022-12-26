$(document).ready(function(){

    $("#btn_upload").click(function(){
        var fd = new FormData();
        var files = $('#file')[0].files;
        var user_stop_list = $('#user_stop_list').val().trim();
        var result_file_name = $('#result_file_name').val().trim();
        var counter_type = $('#counter_type').val().trim();
        var timespan_type = $('#timespan_type').val().trim();
        console.log("Stop list:");
        console.log(user_stop_list);
        console.log("Counter type:");
        console.log(counter_type);
        console.log("Timespan type:");
        console.log(timespan_type);
        // Check file selected or not
        if (files.length > 0) {
           fd.append('file', files[0]);
           fd.append('user_stop_list', user_stop_list);
           fd.append('result_file_name', result_file_name);
           fd.append('counter_type', counter_type);
           fd.append('timespan_type', timespan_type);

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