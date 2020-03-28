function init() {
    var main_frame = document.getElementById("video-container");
    var fw = main_frame.clientWidth||main_frame.offsetWidth;
    vw = fw * 0.4;
    vh = fw * 0.3;
    var video = document.getElementById("video-container");
    video.style.width = vw + "px";
    video.style.height = vh + "px";
    var html = "<svg class='bi bi-person' width='100%' height='100%' viewBox='0 0 20 20' fill='#00CED1' " +
        "xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M15 16s1 0 1-1-1-4-6-4-6 3-6 4 1 1 1 " +
        "1h10zm-9.995-.944v-.002zM5.022 15h9.956a.274.274 0 00.014-.002l.008-.002c-.001-.246-.154-.986-.832-1.664C13.516" +
        " 12.68 12.289 12 10 12c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664a1.05 1.05 " +
        "0 00.022.004zm9.974.056v-.002zM10 9a2 2 0 100-4 2 2 0 000 4zm3-2a3 3 0 11-6 0 3 3 0 016 0z' " +
        "clip-rule='evenodd'></path></svg>";
    video.innerHTML = html;
}

function record() {
    var v = document.getElementById("video-container");
    v.innerHTML = "<video id='video' width='" + vw + "px' height='" + vh + "px'></video>";
    let constraints = {video:true, audio:false};
    let video = document.getElementById("video");
    let promise = navigator.mediaDevices.getUserMedia(constraints);
    promise.then(function(MediaStream) {
        video.srcObject = MediaStream;
        video.play();
    });

}

async function setBack() {
    mediaRecorder.stream.stop();
    await sleep(3000);
    var html = "<svg class='bi bi-person' width='100%' height='100%' viewBox='0 0 20 20' fill='#00CED1' " +
        "xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' d='M15 16s1 0 1-1-1-4-6-4-6 3-6 4 1 1 1 " +
        "1h10zm-9.995-.944v-.002zM5.022 15h9.956a.274.274 0 00.014-.002l.008-.002c-.001-.246-.154-.986-.832-1.664C13.516" +
        " 12.68 12.289 12 10 12c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664a1.05 1.05 " +
        "0 00.022.004zm9.974.056v-.002zM10 9a2 2 0 100-4 2 2 0 000 4zm3-2a3 3 0 11-6 0 3 3 0 016 0z' " +
        "clip-rule='evenodd'></path></svg>";
    v.innerHTML = html;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}
