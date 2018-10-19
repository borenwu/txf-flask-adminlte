;
var account_set_ops = {
	init: function () {
		this.eventBind();
	},
	eventBind: function () {
		$(".wrap_account_set .save").click(function () {
			var btn_target = $(this);
			if (btn_target.hasClass("disabled")) {
				common_ops.alert("正在处理!!请不要重复提交~~");
				return;
			}

			var community_id = $(".wrap_account_set select[name=community]").val();
			var community_name = $(".wrap_account_set select[name=community]").find("option:selected").text();

			var platform_id = $(".wrap_account_set input[name=platform_id]").val();
			var platform_name = $(".wrap_account_set input[name=platform_name]").val();


			var nickname_target = $(".wrap_account_set input[name=nickname]");
			var nickname = nickname_target.val();

			var mobile_target = $(".wrap_account_set input[name=mobile]");
			var mobile = mobile_target.val();

			var email_target = $(".wrap_account_set input[name=email]");
			var email = email_target.val();

			var login_name_target = $(".wrap_account_set input[name=login_name]");
			var login_name = login_name_target.val();

			var login_pwd_target = $(".wrap_account_set input[name=login_pwd]");
			var login_pwd = login_pwd_target.val();

			var benefit_target = $(".wrap_account_set input[name=benefit]");
			var benefit = benefit_target.val()


			if (community_id.length == -1) {
				common_ops.tip("请选择社区~~", community_id);
				return false;
			}

			if (nickname.length < 1) {
				common_ops.tip("请输入符合规范的姓名~~", nickname_target);
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

			if(benefit == ""){
				benefit = 0
			}


			btn_target.addClass("disabled");

			var data = {
				platform_id:platform_id,
				platform_name:platform_name,
				community_id: community_id,
				community_name: community_name,
				nickname: nickname,
				mobile: mobile,
				email:email,
				login_name: login_name,
				login_pwd: login_pwd,
				benefit:benefit,
				id: $(".wrap_account_set input[name=id]").val()
			};

			$.ajax({
				url: common_ops.buildUrl("/account/set"),
				type: 'POST',
				data: data,
				dataType: 'json',
				success: function (res) {
					btn_target.removeClass("disabled");
					var callback = null;
					if (res.code == 200) {
						callback = function () {
							window.location.href = common_ops.buildUrl("/account/index");
						}
					}
					common_ops.alert(res.msg, callback);
				}
			});


		});
	}
};

$(document).ready(function () {
	account_set_ops.init();
});