function init() {
    $("#mny").slider({
        ticks: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ticks_labels: ['$0', '$1', '$2', '$3', '$4', '$5', '$6', '$7', '$8', '$9', '$10'],
        ticks_snap_bounds: 1
    });
}

function init_phase2() {
    var main_frame = document.getElementById("video-container");
    var fw = main_frame.clientWidth||main_frame.offsetWidth;
    vw = fw * 0.35;
    vh = fw * 0.25;
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
    init();
}

function phase1_fb() {
    document.body.innerHTML += "<div style='position:fixed;top:0;width:100%;height:100%;background-color:" +
    "rgba(255, 255, 255, 0.89);color:#00868B;text-align:center;display:table;'>" +
    "<div style='display:table-cell;vertical-align:middle;'>" +
    "<h2>Picking up a partner for you, wait a second...</h2></div></div>";
    setTimeout("javascript:location.href='./phase2-intro.html'", 2000);
}

function phase1_st() {
    document.body.innerHTML += "<div style='position:fixed;top:0;width:100%;height:100%;background-color:" +
    "rgba(255, 255, 255, 0.89);color:#00868B;text-align:center;display:table;'>" +
    "<div style='display:table-cell;vertical-align:middle;'>" +
    "<h2>Picking up a partner for you, wait a second...</h2></div></div>";
    setTimeout("javascript:location.href='./phase1-p.html'", 2000);
}

function phase2_fb() {
    setTimeout("javascript:location.href='./final.html'", 4000);
}



