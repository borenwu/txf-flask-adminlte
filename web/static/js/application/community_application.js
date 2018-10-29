;
var community_application_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this
        $(".wrap_search select[name=application_status]").change(function () {
            $(".wrap_search").submit();
        });
        $("#approve").click(function () {
            that.approve($(this).attr("data"))
        })
    },

    approve: function (id) {
        console.log(id)
        $.ajax({
            url: common_ops.buildUrl("/application/community_application/approve"),
            type: 'POST',
            data: {
                id: id
            },
            dataType: 'json',
            success: function (res) {
                var callback = null;
                if (res.code == 200) {
                    callback = function () {
                        window.location.href = window.location.href;
                    }
                }
                common_ops.alert(res.msg, callback);
            }
        });
    }
};

$(document).ready(function () {
    community_application_ops.init();
});