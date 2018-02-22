$("body").click(function (e) {
        if(e.target.id === "search"){
            $(".section-2")[0].style.display = "none";
            $(".section-3")[0].style.display = "none";
            $(".section-4")[0].style.display = "none";
            $(".section-5")[0].style.display = "none";
            $(".imgs")[0].style.display = "none";

        }
        else {
            $(".section-2")[0].style.display = "block";
            $(".section-3")[0].style.display = "block";
            $(".section-4")[0].style.display = "block";
            $(".section-5")[0].style.display = "block";
            $(".imgs")[0].style.display = "inherit";

        }
    })