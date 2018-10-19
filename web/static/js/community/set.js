;
var community_set_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $(".wrap_account_set .save").click(function(){
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var name_target = $(".wrap_account_set input[name=name]");
            var name = name_target.val();

            var province_target = $(".wrap_account_set input[name=province]");
            var province = province_target.val();

            var city_target = $(".wrap_account_set input[name=city]");
            var city = city_target.val();

            var description_target = $(".wrap_account_set input[name=description]");
            var description = description_target.val();

            var pickups_target = $(".wrap_account_set input[name=pickups]");
            var pickups = pickups_target.val();

            if( name.length < 1 ){
                common_ops.tip( "请输入符合规范的社区名~~",name_target );
                return false;
            }

            if( province.length < 1 ){
                common_ops.tip( "请输入符合规范的省份~~",province_target );
                return false;
            }

            if(  city.length < 1 ){
                common_ops.tip( "请输入符合规范的城市~~",city_target );
                return false;
            }

            if( description.length < 1 ){
                common_ops.tip( "请输入符合规范的社区简介~~",description_target );
                return false;
            }

            if( pickups.length < 2 ){
                common_ops.tip( "请输入符合规范的自提点信息~~",pickups_target );
                return false;
            }

            btn_target.addClass("disabled");

            var data = {
                name: name,
                province: province,
                city: city,
                description:description,
                pickups:pickups,
                id:$(".wrap_account_set input[name=id]").val()
            };

            $.ajax({
                url:common_ops.buildUrl( "/community/set" ),
                type:'POST',
                data:data,
                dataType:'json',
                success:function( res ){
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function(){
                            window.location.href = common_ops.buildUrl("/community/index");
                        }
                    }
                    common_ops.alert( res.msg,callback );
                }
            });


        });
    }
};

$(document).ready( function(){
    community_set_ops.init();
} );