;
var leader_application_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this
        $(".wrap_search select[name=application_status]").change(function () {
            $(".wrap_search").submit();
        });

    },

};

$(document).ready(function () {
    leader_application_ops.init();
});