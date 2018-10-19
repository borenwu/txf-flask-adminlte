;
var user_login_ops = {
        init: function () {
            this.eventBind();
        },

        is_weixn: function () {
            var ua = navigator.userAgent.toLowerCase();
            if (ua.match(/MicroMessenger/i) == "micromessenger") {
                return true;
            } else {
                return false;
            }
        },


        eventBind: function () {
            $(".login_wrap .do-login").click(function () {
                var btn_target = $(this);
                if (btn_target.hasClass("disabled")) {
                    common_ops.alert("正在处理!!请不要重复提交~~");
                    return;
                }

                var platform_id = $(".login_wrap select[name=platform]").val();
                var login_name = $(".login_wrap input[name=login_name]").val();
                var login_pwd = $(".login_wrap input[name=login_pwd]").val();


                if (platform_id == -1) {
                    common_ops.alert("请选择平台");
                    return;
                }
                if (login_name == undefined || login_name.length < 1) {
                    common_ops.alert("请输入正确的登录用户名~~");
                    return;
                }
                if (login_pwd == undefined || login_pwd.length < 1) {
                    common_ops.alert("请输入正确的密码~~");
                    return;
                }
                btn_target.addClass("disabled");
                $.ajax({
                    url: common_ops.buildUrl("/user/login"),
                    type: 'POST',
                    data: {'login_name': login_name, 'login_pwd': login_pwd, 'platform_id': platform_id},
                    dataType: 'json',
                    success: function (res) {
                        btn_target.removeClass("disabled");
                        var callback = null;
                        if (res.code == 200) {
                            callback = function () {
                                window.location.href = common_ops.buildUrl("/");
                            }
                        }
                        common_ops.alert(res.msg, callback);
                    }
                });
            });
        }
    }
;

$(document).ready(function () {
    user_login_ops.init();
});