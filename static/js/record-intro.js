function intro_init() {
    var main_frame = document.getElementById("video-container");
    // var fw = main_frame.clientWidth||main_frame.offsetWidth;
    vw = 480;
    vh = 360;
    main_frame.style.width = vw + "px";
    main_frame.style.height = vh + "px";
    main_frame.innerHTML = "<video id='video' width='" + vw + "px' height='" + vh + "px'></video>";
    let constraints = {video:{ width: 480, height: 360 }, audio:false};
    let video = document.getElementById("video");
    let promise = navigator.mediaDevices.getUserMedia(constraints);
    promise.then(function(MediaStream) {
        video.srcObject = MediaStream;
        video.play();
    });
}