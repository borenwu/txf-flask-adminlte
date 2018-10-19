;
var finance_index_ops = {
    init: function () {
        this.eventBind();
        this.datetimepickerComponent();
    },
    eventBind: function () {
        var that = this;
        // $(".wrap_search select[name=community_name]").change( function(){
        //     $(".wrap_search").submit();
        // });

        $(".wrap_search .search").click(function () {
            $(".wrap_search").submit();
        });

        $(".wrap_search .download").click(function () {
            console.log('download')
            $(".table2excel").table2excel({
                // 不被导出的表格行的CSS class类
                exclude: ".noExl",
                // 导出的Excel文档的名称
                name: "Excel Document Name",
                // Excel文件的名称
                filename: "财务报告" + new Date().toISOString().replace(/[\-\:\.]/g, ""),
                //文件后缀名
                // fileext: ".xls",
                //是否排除导出图片
                exclude_img: true,
                //是否排除导出超链接
                exclude_links: true,
                //是否排除导出输入框中的内容
                exclude_inputs: true
            });
        });
    },

    datetimepickerComponent: function () {
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
            format: 'Y-m-d',//格式化显示
            timepicker: false
        };
        $('.wrap_search input[name=date_from]').datetimepicker(params);
        $('.wrap_search input[name=date_to]').datetimepicker(params);

    },
};

$(document).ready(function () {
    finance_index_ops.init();
});