var base_url = ""

function setUploadEnable() {
    document.getElementById("upload").disabled = false;
}

function setUploadDisable() {
    document.getElementById("upload").disabled = true;
}

function setTakePhotoEnable() {
    document.getElementById("snap").disabled = false;
}

function setTakePhotoDisable() {
    document.getElementById("snap").disabled = true;
}

function setRemoveEnable() {
    document.getElementById("remove").disabled = false;
}

function setRemoveDisable() {
    document.getElementById("remove").disabled = true;
}

function setNextEnable() {
    document.getElementById("next").disabled = false;
}

function setNextDisable() {
    document.getElementById("next").disabled = true;
}

function setAllDisable() {
    setNextDisable();
    setRemoveDisable();
    setTakePhotoDisable();
    setUploadDisable();
}

function init() {
    setAllDisable();

    var main_frame = document.getElementById("video-container");
    var snap = document.getElementById("snap");
    var rmv = document.getElementById("remove");
    var upload = document.getElementById("upload");
    var fw = main_frame.clientWidth||main_frame.offsetWidth;
    vw = 640;
    vh = 480;
    main_frame.style.width = vw + "px";
    main_frame.style.height = vh + "px";
    main_frame.innerHTML = "<video id='video' width='" + vw + "px' height='" + vh + "px'></video>";
    let constraints = {video:true, audio:false};
    let video = document.getElementById("video");
    let promise = navigator.mediaDevices.getUserMedia(constraints);
    promise.then(function(MediaStream) {
        setTakePhotoEnable();
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
        setTakePhotoDisable();
        setRemoveEnable();
        setUploadEnable();
    });
    rmv.addEventListener('click', function() {
        setRemoveDisable();
        setUploadDisable();
        setNextDisable();
        main_frame.innerHTML = "<video id='video' width='" + vw + "px' height='" + vh + "px'></video>";
        let video = document.getElementById("video");
        let promise = navigator.mediaDevices.getUserMedia(constraints);
        promise.then(function(MediaStream) {
            setTakePhotoEnable();
            video.srcObject = MediaStream;
            video.play();
        });
    });
    upload.addEventListener('click', function() {
        var canvas = document.getElementById("canvas");
        var imgData = canvas.toDataURL("image/jpg");
        var base64Data = imgData.substring(22);
        document.getElementById('upload-text').style.visibility = 'visible';
	    $.ajax({
	        url: base_url + "/submit_pic",
	        data: {"img": base64Data},
	        type: 'POST',
	        success: function(result) {
                setUploadDisable();
                setNextEnable();
                document.getElementById('upload-text').style.visibility = 'hidden';
                alert(result);
            }
        });
    });
}

function submit_pic() {
    location.href='/phase1-2';
}
