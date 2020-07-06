$(document).ready(function () {
    // OUTER-LAYOUT
    $('body').layout({
        center__paneSelector:	    "#centerWindow",
        east__paneSelector:		"#instanceWindow",
        east__size:				450,
        spacing_open:			    8,  // ALL panes
        spacing_closed:			12, // ALL panes
        north__maxSize:			200,
        south__maxSize:			200,
        center__childOptions: {
            center__paneSelector: "#textWindow",
            south__paneSelector: "#nodeInfoWindow",
            west__paneSelector: "#contentWindow",
            south__size: 250,
            west__size:200,
            spacing_open: 8,  // ALL panes
            spacing_closed: 12 // ALL panes
        },
        east__childOptions: {
            center__paneSelector: "#instanceSelectWindow",
            south__paneSelector: "#instancInfoWindow",
            south__size: 330,
            spacing_open: 8,  // ALL panes
            spacing_closed: 12,// ALL panes
        }
        // ,
        // onresize : (function(){
        //     var h = $(".textWindow").height()
        //     alert(h)
        //     $(".textTab").height("50px");
        // })()
    });

});
