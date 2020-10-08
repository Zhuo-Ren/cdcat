$(document).ready(function () {
    // OUTER-LAYOUT
    $('body').layout({
        center__paneSelector:	"#textWindow",
        east__paneSelector:		"#eastWindow",
        west__paneSelector:     "#catalogueWindow",
        west__size:				200,  // size of west window
        east__size:				800,  // size of east window
        spacing_open:			    8,  // ALL panes
        spacing_closed:			12, // ALL panes
        north__maxSize:			200,
        south__maxSize:			200,
        east__childOptions: {
            center__paneSelector: "#annotationWindow",
            east__paneSelector: "#instanceSelectWindow",
            east__size: 300,    // size of east window
            spacing_open: 8,  // ALL panes
            spacing_closed: 12,// ALL panes
            center__childOptions: {
                center__paneSelector: "#nodeInfoWindow",
                south__paneSelector: "#instanceInfoWindow",
                south__size: 400,
                spacing_open: 8,  // ALL panes
                spacing_closed: 12,// ALL panes
            }
        }
    });

});
