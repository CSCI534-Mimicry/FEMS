var base_url = ""

function init() {
    var main_frame = document.getElementById("video-container");
    var snap = document.getElementById("snap");
    var rmv = document.getElementById("remove");
    var upload = document.getElementById("upload");
    var fw = main_frame.clientWidth||main_frame.offsetWidth;
    vw = fw * 0.4;
    vh = fw * 0.3;
    main_frame.style.width = vw + "px";
    main_frame.style.height = vh + "px";
    main_frame.innerHTML = "<video id='video' width='" + vw + "px' height='" + vh + "px'></video>";
    let constraints = {video:true, audio:false};
    let video = document.getElementById("video");
    let promise = navigator.mediaDevices.getUserMedia(constraints);
    promise.then(function(MediaStream) {
        video.srcObject = MediaStream;
        video.play();
    });
    snap.addEventListener('click', function() {
        let video = document.getElementById("video");
        main_frame.innerHTML = "<canvas id='canvas' width='" + vw + "px' height='" + vh + "px'></canvas>";
        let canvas = document.getElementById("canvas");
        canvas.getContext('2d').drawImage(video, 0, 0, vw, vh);
        var image = new Image();
	    image.src = canvas.toDataURL("image/jpg");
    });
    rmv.addEventListener('click', function() {
        main_frame.innerHTML = "<video id='video' width='" + vw + "px' height='" + vh + "px'></video>";
        let video = document.getElementById("video");
        let promise = navigator.mediaDevices.getUserMedia(constraints);
        promise.then(function(MediaStream) {
            video.srcObject = MediaStream;
            video.play();
        });
    });
    upload.addEventListener('click', function() {
        var canvas = document.getElementById("canvas");
        var imgData = canvas.toDataURL("image/jpg");
        var base64Data = imgData.substring(22);
	    $.ajax({
	        url: base_url + "/submit_pic",
	        data: {"img": base64Data},
	        type: 'POST',
	        success: function(result) {
                alert(result);
            }
        });
    });
}

function submit_pic() {
    var canvas = document.getElementById("canvas");
    if (canvas != null) {
        var imgData = canvas.toDataURL("image/jpg");
        var base64Data = imgData.substring(22);
	    $.ajax({
	        url: base_url + "/submit_pic",
	        data: {"img": base64Data},
	        type: 'POST',
	        success: function(result) {}
        });
    }
    setTimeout("javascript:location.href='/phase1-2'", 500);
}
