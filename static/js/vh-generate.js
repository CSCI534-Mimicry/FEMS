function vh_generation() {
    $.ajax({
	    url: "/generate-action-units",
	    type: 'GET',
	    success: function(result) {}
    });
}

function vh_generation_one_pic() {
    $.ajax({
	    url: "/generate-action-units-one-pic",
	    type: 'GET',
	    success: function(result) {}
    });
}

function vh_files_check() {
    $.ajax({
	    url: "/check-output-files",
	    type: 'GET',
	    success: function(result) {
            setTimeout("javascript:location.href='/phase2-1'", 500);
        }
    });
}