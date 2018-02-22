$(document).ready(function () {
    $('.carousel').carousel({
        interval:2000,
        pause:"hover",
        warp:true
    });

    // $('.carousel-caption')[0].style.display = "none";
    // console.log($('.carousel-img'));
    console.log($(window).width());
    if($(window).width() < 768){
        $('.carousel-img').each(function () {
            // console.log($(this)[0].src="img/abigail-keenan-27292-s333r-1.jpg")
        })
    }
    $('.carousel-img').hover(function () {
        // $(this).css("display" ,"inherit");

       $($(this)[0].nextElementSibling)[0].style.display="inherit";
       $(this)[0].style.opacity = 0.5;
    },function () {
        $('.carousel-caption').each(function () {
            $(this)[0].style.display = 'none';
            $($(this)[0].previousElementSibling)[0].style.opacity = 1;
            // console.log($(this));
        });
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