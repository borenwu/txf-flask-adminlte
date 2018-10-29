;
var leader_application_info_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this

        $(".wrap_account_set .save").click(function () {

            var member_id_target = $(".wrap_account_set input[name=member_id]");
            var member_id = member_id_target.val();

            var province_target = $(".wrap_account_set input[name=province]");
            var province = province_target.val();

            var city_target = $(".wrap_account_set input[name=city]");
            var city = city_target.val();

            var community_name_target = $(".wrap_account_set input[name=community_name]");
            var community_name = community_name_target.val();


            var pickups_target = $(".wrap_account_set input[name=pickups]");
            var pickups = pickups_target.val();

            var description_target = $(".wrap_account_set input[name=description]");
            var description = description_target.val();

            var name_target = $(".wrap_account_set input[name=name]");
            var name = name_target.val();

            var mobile_target = $(".wrap_account_set input[name=mobile]");
            var mobile = mobile_target.val();

            var login_name_target = $(".wrap_account_set input[name=login_name]");
            var login_name = login_name_target.val();

            var login_pwd_target = $(".wrap_account_set input[name=login_pwd]");
            var login_pwd = login_pwd_target.val();


            if (name.length < 1) {
                common_ops.tip("请输入符合规范的姓名~~", name_target);
                return false;
            }


            if (mobile.length < 1) {
                common_ops.tip("请输入符合规范的手机号码~~", mobile_target);
                return false;
            }


            if (login_name.length < 1) {
                common_ops.tip("请输入符合规范的登录用户名~~", login_name_target);
                return false;
            }

            if (login_pwd.length < 3) {
                common_ops.tip("请输入符合规范的登录密码~~", login_pwd_target);
                return false;
            }

            $.ajax({
                url: common_ops.buildUrl("/application/leader_application/approve"),
                type: 'POST',
                data: {
                    member_id:member_id,
                    province:province,
                    city:city,
                    community_name:community_name,
                    pickups:pickups,
                    description:description,
                    name:name,
                    mobile:mobile,
                    login_name:login_name,
                    login_pwd:login_pwd,
                    id: $(".wrap_account_set input[name=id]").val()
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
        })
    },

    approve: function () {
        console.log('approve')
        // $.ajax({
        //     url: common_ops.buildUrl("/application/leader_application/approve"),
        //     type: 'POST',
        //     data: {
        //         id: id
        //     },
        //     dataType: 'json',
        //     success: function (res) {
        //         var callback = null;
        //         if (res.code == 200) {
        //             callback = function () {
        //                 window.location.href = window.location.href;
        //             }
        //         }
        //         common_ops.alert(res.msg, callback);
        //     }
        // });
    }
};

$(document).ready(function () {
    leader_application_info_ops.init();
});