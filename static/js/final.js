function showSuccess() {
    document.getElementById('feedback-submit').innerHTML += `<div class="fems-msg alert alert-success" style="width: 60%; margin:0 auto; margin-top: 15px" role="alert">
        <strong>Successfully submitted!</strong> Thank you for your feedback!
    </div>`;
}

function showError() {
    document.getElementById('feedback-submit').innerHTML += `<div class="fems-msg alert alert-danger" style="width: 60%; margin:0 auto; margin-top: 15px" role="alert">
        <strong>Oh snap!</strong> Submit error. Please try again.
    </div>`;
}

function showEmpty() {
    document.getElementById('feedback-submit').innerHTML += `<div class="fems-msg alert alert-danger" style="width: 60%; margin:0 auto; margin-top: 15px" role="alert">
        <strong>Oh no!</strong> Please don't submit empty feedback!
    </div>`;
}

function submit_feedback() {
    $('.fems-msg').hide();
    var val = document.getElementById('feedback').value;
    if(val == "") showEmpty();
    else {
        $.ajax({
            url: "/submit-feedback",
            data: {"feedback": val},
            type: 'POST',
            success: function(result) {
                showSuccess();
                document.getElementById('feedback').value = val;
            },
            error: function(result) {
                showError();
                document.getElementById('feedback').value = val;
            }
        });
    }
}