(function($) {
    "use strict";
    $(function () {
        for (var nk = window.location, o = $(".nano-content li a").filter(function () {
            return this.href == nk;
        })
            .addClass("active")
            .parent()
            .addClass("active"); ;) {
            if (!o.is("li")) break;
            o = o.parent()
                .addClass("d-block")
                .parent()
                .addClass("active");
        }
    });
})(jQuery);

(function($) {
    "use strict";
    $(function () {
        $(".btn-plot").each(function() {
            if ($(this).data('delta') < 5) {
                $(this).removeClass();
                $(this).addClass("btn btn-info btn-plot badge-primary");
            } else {
                $(this).removeClass();
                $(this).addClass("btn btn-info btn-plot badge-danger");
            }
        });
    });
})(jQuery);