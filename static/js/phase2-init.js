function showEmailSubmit() {
    document.getElementById('email-submit').style.visibility = 'visible';
}

function showThankyou() {
    document.getElementById('email-submit').innerHTML = `<div class="alert alert-success" style="width: 60%; margin:0 auto" role="alert">
        <strong>Successfully submitted!</strong> Please check your email within 24 hours for next step or just wait here without refreshing this page. 
        Thank you for your participance and patience.
    </div>`;
}

function showError() {
    document.getElementById('email-submit').innerHTML += `<div class="fems-error alert alert-danger" style="width: 60%; margin:0 auto" role="alert">
        <strong>Oh snap!</strong> Submit error. Please try again.
    </div>`;
}


function showEmailError() {
    document.getElementById('email-submit').innerHTML += `<div class="fems-error alert alert-danger" style="width: 60%; margin:0 auto" role="alert">
        <strong>Error:</strong> Please check your input. It should be your email address.
    </div>`;
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function emailSubmit() {
    $('.fems-error').hide();
    var email = document.getElementById("personal-email").value;
    if(validateEmail(email)) {
        $.ajax({
            url: base_url + "/get-user-email",
            data: {"email": email},
            type: 'POST',
            success: function(result) {
                showThankyou();
            },
            error: function(result) {
                showError();
            }
        });
    }
    else {
        showEmailError();
    }
}

function phase2_init() {
    setTimeout(function() {
        showEmailSubmit();
    }, 8000);
}