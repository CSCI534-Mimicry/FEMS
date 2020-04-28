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
}

function drawVideoImageScaled(img, ctx) {
    var canvas = ctx.canvas ;
    var img_width = img.srcObject.getVideoTracks()[0].getSettings().width;
    var img_height = img.srcObject.getVideoTracks()[0].getSettings().height;
    var hRatio = canvas.width  / img_width   ;
    var vRatio =  canvas.height / img_height  ;
    var ratio  = Math.min ( hRatio, vRatio );
    var centerShift_x = ( canvas.width - img_width*ratio ) / 2;
    var centerShift_y = ( canvas.height - img_height*ratio ) / 2;  
    ctx.clearRect(0,0,canvas.width, canvas.height);
    ctx.drawImage(img, 0,0, img_width, img_height,
                       centerShift_x,centerShift_y,img_width*ratio, img_height*ratio);  
 }

function init() {
    setAllDisable();

    var main_frame = document.getElementById("video-container");
    var snap = document.getElementById("snap");
    var rmv = document.getElementById("remove");
    var fw = main_frame.clientWidth||main_frame.offsetWidth;
    vw = 480;
    vh = 360;
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
        drawVideoImageScaled(video, canvas.getContext('2d'));
        // canvas.getContext('2d').drawImage(video, 0, 0, video.width, video.height, 0, 0, video.width*ratio, video.height*ratio);
        var image = new Image();
        image.src = canvas.toDataURL("image/jpg");
        setTakePhotoDisable();
        setRemoveEnable();
        setNextEnable();
    });
    rmv.addEventListener('click', function() {
        setRemoveDisable();
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
}

function upload_pic() {
    var canvas = document.getElementById("canvas");
    var imgData = canvas.toDataURL("image/jpg");
    var base64Data = imgData.substring(22);
    document.getElementById('upload-text').style.visibility = 'visible';
    setNextDisable();
    $.ajax({
        url: base_url + "/submit_pic",
        data: {"img": base64Data},
        type: 'POST',
        success: function(result) {
            document.getElementById('upload-text').innerHTML = 'Upload success! Proceeding...';
            setTimeout(function(){
                submit_pic();
            }, 1000); 
        },
        error: function(result) {
            setNextEnable();
            document.getElementById('upload-text').style.visibility = 'hidden';
            alert("Photo upload error. Please try again.");
        }
    });
}

function submit_pic() {
    location.href='/phase1-2';
}
