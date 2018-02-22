$(document).ready(function () {
    $('.carousel').carousel({
        interval:2000,
        pause:"hover",
        warp:true
    });

//    Search click
    $("body").click(function (e) {
        if(e.target.id === "search"){
            $(".section-1")[0].style.display = "none";
            $(".section-3")[0].style.display = "none";
            $(".section-4")[0].style.display = "none";

        }
        else {
            $(".section-1")[0].style.display = "block";
            $(".section-3")[0].style.display = "block";
            $(".section-4")[0].style.display = "block";

        }
    })
});