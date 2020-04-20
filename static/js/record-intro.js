var base_url = ""

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

function setAllDisable() {
    setRemoveDisable();
    setTakePhotoDisable();
}

function init() {
    setAllDisable();

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
    });
    rmv.addEventListener('click', function() {
        setRemoveDisable();
        main_frame.innerHTML = "<video id='video' width='" + vw + "px' height='" + vh + "px'></video>";
        let video = document.getElementById("video");
        let promise = navigator.mediaDevices.getUserMedia(constraints);
        promise.then(function(MediaStream) {
            setTakePhotoEnable();
            video.srcObject = MediaStream;
            video.play();
        });
    });
}