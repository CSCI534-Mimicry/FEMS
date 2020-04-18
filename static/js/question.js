var base_url = "";
var sex = "male";
var age = "<18";
var race = "White"
function set_sex(obj) {
    sex = obj;
}

function set_age(obj) {
    age = obj;
}

function set_race(obj) {
    race = obj;
}

function submit_question() {
    $.ajax({
	    url: base_url + "/submit_question",
	    data: {"sex": sex, "age": age, "race": race},
	    type: 'POST',
	    success: function(result) {
            location.href='./phase1-intro.html';
        }
    });
}