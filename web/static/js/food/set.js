;
var upload = {
    error: function (msg) {
        common_ops.alert(msg);
    },
    success: function (file_key) {
        console.log("success")
        console.log(file_key)
        if (!file_key) {
            return;
        }
        var html = '<img src="' + file_key + '"/>'
            + '<span class="fa fa-times-circle del del_image" data="' + file_key + '"></span>';
        $(".upload_pic_wrap").append('<span class="pic-each">' + html + '</span>');

        // if ($(".upload_pic_wrap .pic-each").size() > 0) {
        //     $(".upload_pic_wrap .pic-each").html(html);
        // } else {
        //     $(".upload_pic_wrap").append('<span class="pic-each">' + html + '</span>');
        // }
        food_set_ops.delete_img();
    }
};
var food_set_ops = {
    init: function () {
        this.ue = null;
        this.eventBind();
        this.initEditor();
        this.delete_img();
        this.datetimepickerComponent();
    },
    datetimepickerComponent:function(){
        var that = this;
        $.datetimepicker.setLocale('zh');
        params = {
            scrollInput: false,
            scrollMonth: false,
            scrollTime: false,
            dayOfWeekStart: 1,
            lang: 'zh',
            todayButton: true,//回到今天
            defaultSelect: true,
            defaultDate: new Date().Format('yyyy-MM-dd'),
            format: 'Y-m-d H:i:s',//格式化显示
            timepicker: true
        };
        $('.wrap_food_set input[name=date_from]').datetimepicker(params);
        $('.wrap_food_set input[name=date_to]').datetimepicker(params);

    },
    eventBind: function () {
        var that = this;

        $(".wrap_food_set .upload_pic_wrap input[name=pic]").change(function () {
            $(".wrap_food_set .upload_pic_wrap").submit();
        });

        $(".wrap_food_set select[name=cat_id]").select2({
            language: "zh-CN",
            width: '100%'
        });

        $(".wrap_food_set select[name=ratio]").select2({
            language: "zh-CN",
            width: '100%'
        });

        $("#communities").doublebox({
            nonSelectedListLabel: '待选择社区',
            selectedListLabel: '选中社区',
            preserveSelectionOnMove: 'moved',
            moveOnSelect: false,
            optionValue: "roleId",
            optionText: "roleName",
            doubleMove: true,
        });

        $(".wrap_food_set input[name=tags]").tagsInput({
            width: 'auto',
            height: 40,
            onAddTag: function (tag) {
            },
            onRemoveTag: function (tag) {
            }
        });

        $(".wrap_food_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var cat_id_target = $(".wrap_food_set select[name=cat_id]");
            var cat_id = cat_id_target.val();

            var platform_id = $("#platform_id").val();
			var platform_name = $("#platform_name").val();

			var date_from = $('.wrap_food_set input[name=date_from]').val()
            var date_to = $('.wrap_food_set input[name=date_to]').val()

			var communities_target = $("#communities").val()
            var communities = communities_target.join(",")

            var name_target = $(".wrap_food_set input[name=name]");
            var name = name_target.val();

            var ratio_target = $(".wrap_food_set select[name=ratio]");
            var ratio = ratio_target.val();

            var market_price_target = $(".wrap_food_set input[name=market_price]");
            var market_price = market_price_target.val();

            var price_target = $(".wrap_food_set input[name=price]");
            var price = price_target.val();

            var limit_quantity_target = $(".wrap_food_set input[name=limit_quantity]");
            var limit_quantity = limit_quantity_target.val();

            var summary = $.trim(that.ue.getContent());

            var stock_target = $(".wrap_food_set input[name=stock]");
            var stock = stock_target.val();

            var tags_target = $(".wrap_food_set input[name=tags]");
            var tags = $.trim(tags_target.val());

            if (parseInt(cat_id) < 1) {
                common_ops.tip("请选择分类~~", cat_id_target);
                return;
            }

            if (date_from.length < 1) {
                common_ops.alert("请输入开始日期~~");
                return;
            }

            if (date_to.length < 1) {
                common_ops.alert("请输入结束日期~~");
                return;
            }

            if (communities.length < 1) {
                common_ops.alert("请选择社区~~");
                return;
            }

            if (name.length < 1) {
                common_ops.alert("请输入符合规范的名称~~");
                return;
            }

            if (parseFloat(ratio) <= 0) {
                common_ops.tip("请输入符合规范的提成比例~~", price_target);
                return;
            }

            if (parseFloat(market_price) <= 0) {
                common_ops.tip("请输入符合规范的售卖价格~~", price_target);
                return;
            }

            if (parseFloat(price) <= 0) {
                common_ops.tip("请输入符合规范的售卖价格~~", price_target);
                return;
            }

            if ($(".wrap_food_set .pic-each").size() < 1) {
                common_ops.alert("请上传封面图~~");
                return;
            }

            if (summary.length < 10) {
                common_ops.tip("请输入描述，并不能少于10个字符~~", price_target);
                return;
            }

            if (parseInt(stock) < 1) {
                common_ops.tip("请输入符合规范的库存量~~", stock_target);
                return;
            }

            if (tags.length < 1) {
                common_ops.alert("请输入标签，便于搜索~~");
                return;
            }

            btn_target.addClass("disabled");

            var data = {
                cat_id: cat_id,
                platform_id:platform_id,
                platform_name:platform_name,
                date_from:date_from,
                date_to:date_to,
                communities:communities,
                name: name,
                ratio:ratio,
                market_price:market_price,
                price: price,
                limit_quantity:limit_quantity,
                main_image: $(".wrap_food_set .pic-each .del_image").attr("data"),
                summary: summary,
                stock: stock,
                tags: tags,
                id: $(".wrap_food_set input[name=id]").val()
            };

            $.ajax({
                url: common_ops.buildUrl("/food/set"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/food/index");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });

        });


    },
    initEditor: function () {
        var that = this;
        that.ue = UE.getEditor('editor', {
            toolbars: [
                ['undo', 'redo', '|',
                    'bold', 'italic', 'underline', 'strikethrough', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', '|', 'rowspacingtop', 'rowspacingbottom', 'lineheight'],
                ['customstyle', 'paragraph', 'fontfamily', 'fontsize', '|',
                    'directionalityltr', 'directionalityrtl', 'indent', '|',
                    'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'touppercase', 'tolowercase', '|',
                    'link', 'unlink'],
                ['imagenone', 'imageleft', 'imageright', 'imagecenter', '|',
                    'insertimage', 'insertvideo', '|',
                    'horizontal', 'spechars', '|', 'inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols']

            ],
            enableAutoSave: true,
            saveInterval: 60000,
            elementPathEnabled: false,
            zIndex: 4,
            serverUrl: common_ops.buildUrl('/upload/ueditor')
        });
    },
    delete_img: function () {
        $(".wrap_food_set .del_image").unbind().click(function () {
            $(this).parent().remove();
        });
    }
};

$(document).ready(function () {
    food_set_ops.init();
});