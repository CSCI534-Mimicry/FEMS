var emotion = "neutral";
var base_url = "";

function init() {
    emotion = "neutral";
    var total = document.getElementById("data").innerText;
    var data = [];
    var label = [];
    var pos = [];
    var itv = parseInt(total / 10) + 1;
    var count = 0;
    for (var i = 0; i <= total; i += itv) {
        data.push(i);
        label.push("$" + i);
        count++;
    }
    var lp = 0
    if (!(total in data)) {
        lp = total -  data[data.length - 1];
        data.push(total);
        label.push("$" + total);
    }
    var mgn = 100 / ((count - 1) * itv + lp);
    for (var j = 0; j < data.length; j++) {
        pos.push(data[j] * mgn);
    }

    $("#mny").slider({
        ticks: data,
        ticks_positions: pos,
        ticks_labels: label,
        ticks_snap_bounds: 1 / itv,
        formatter: function(value) {
		    return 'Share $' + value;
	    },
	    value: parseInt(total / 2)
    });
}

var round;
var curr_usr;

function init2() {
    var total = document.getElementById("data").innerText;
    var data = [];
    var label = [];
    var pos = [];
    var itv = parseInt(total / 10) + 1;
    var count = 0;
    for (var i = 0; i <= total; i += itv) {
        data.push(i);
        label.push("$" + i);
        count++;
    }
    var lp = 0
    if (!(total in data)) {
        lp = total -  data[data.length - 1];
        data.push(total);
        label.push("$" + total);
    }
    var mgn = 100 / ((count - 1) * itv + lp);
    for (var j = 0; j < data.length; j++) {
        pos.push(data[j] * mgn);
    }

    $.ajax({
	    url: base_url + "/current_usr",
        type: 'GET',
        async: false,
	    success: function(result) {
            curr_usr = result;
        }
    });

    $.ajax({
	    url: base_url + "/current_sec2_round",
        type: 'GET',
        async: false,
	    success: function(result) {
            round = result;
        }
    });

    $("#mny").slider({
        ticks: data,
        ticks_positions: pos,
        ticks_labels: label,
        ticks_snap_bounds: 1 / itv,
        formatter: function(value) {
		    return 'Share $' + value;
	    },
	    value: 5
    }).on('change', function (e) {
        debounce(handleChange(e.value.newValue), 1);
    });
}

function init3() {

    $(".mny-similar").slider({
        ticks: [1, 2, 3, 4, 5],
        ticks_labels: ["Not similar at all", "Slightly similar", "Moderately similar", "Very similar", "Extremely similar"],
        ticks_snap_bounds: 1,
        value: 1
    });

    $(".mny-human").slider({
        ticks: [1, 2, 3, 4, 5],
        ticks_labels: ["Not at all", "To some extent", "To a moderate extent", "To a large extent", "To an Extremely great extent"],
        ticks_snap_bounds: 1,
        value: 1
    });
}

function handleChange(v) {
    if(round == 0) document.getElementById("face").src = "/img/testers/" + curr_usr + "/gnt/" + v + ".png";
    else document.getElementById("face").src = "/img/testers/" + curr_usr + "/ran/" + v + ".png";
}

function debounce(fn, idle) {
    var last
    return function(){
        var ctx = this, args = arguments
        clearTimeout(last)
        last = setTimeout(function() {
            fn.apply(ctx, args)
        }, idle)
    }
}

function set_emotion(obj) {
    emotion = obj;
}

function update_mny() {
    var mny = document.getElementById("mny").value;
    $.ajax({
	    url: base_url + "/update_mny",
	    data: {"mny": mny},
	    type: 'POST',
	    success: function(result) {
            location.href='/phase2-2';
        }
    });
}

function send_evaluation() {
    var similar = document.getElementById("mny").value;
    var treat = document.getElementById("mny2").value;
    var similar1 = document.getElementById("mny3").value;
    var treat1 = document.getElementById("mny4").value;
    $.ajax({
	    url: base_url + "/submit_evaluation",
	    data: {"similar": similar, "treat": treat, "similar1": similar1, "treat1": treat1},
	    type: 'POST',
	    success: function(result) {
            location.href='/phase2-4';
        }
    });
}

function send_emotion() {
    var mny = document.getElementById("mny").value
    $.ajax({
	    url: base_url + "/submit_emotion",
	    data: {"emotion": emotion, "mny": mny},
	    type: 'POST',
	    success: function(result) {
            vh_generation_one_pic();
            setTimeout("javascript:location.href='/phase1-3'", 500);
        }
    });
}

function pick_partner() {
    setTimeout("javascript:location.href='/phase1-0'", 3000);
}

function phase2_fb() {
    setTimeout("javascript:location.href='/phase2-4'", 3000);
}

function phase2_nt() {
    vh_files_check();
}

function phase2_toq() {
    setTimeout("javascript:location.href='/phase2-3'", 1000);
}


