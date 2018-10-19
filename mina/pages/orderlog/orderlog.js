var app = getApp();
// pages/orderlog/orderlog.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        orders: []
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function(options) {
        var community_name = app.getCache('community').community_name
        wx.setNavigationBarTitle({
            title: community_name + '-接龙凭证'
        });
        wx.showShareMenu({
            withShareTicket: true //要求小程序返回分享目标信息
        })
        this.getOrderLogs()
    },

    onPullDownRefresh: function () {
       this.getOrderLogs()
    },

    getOrderLogs:function(){
        
        var community_name = app.getCache('community').community_name
        wx.setNavigationBarTitle({
            title:community_name + '-接龙凭证'
        });

        var that = this
        var platform_id = app.getCache('platform').platform_id
        var community_id = app.getCache('community').community_id
        wx.request({
            url: app.buildUrl("/member/orderlogs"),
            method:"POST",
            data: {
                platform_id: platform_id,
                community_id: community_id
            },
            header: app.getRequestHeader(),
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({ "content": resp.msg });
                    return;
                }
                var orders = resp.data.order_list;
                that.setData({
                    orders: orders,
                });
            }
        });
    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function() {
        return {
            title: '页面分享标题',
            path: '/pages/orderlog/orderlog',
        }
    }
})