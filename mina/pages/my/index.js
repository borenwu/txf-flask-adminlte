//获取应用实例
var app = getApp();
Page({
    data: {
        community_name:'',
        communities: [],
        visible: false,
    },
    onLoad() {
        var community_name = app.getCache('community').community_name
        this.setData({
            community_name:community_name
        })
        this.getCommunities();
    },
    onShow() {
        this.getInfo();
    },
    getInfo:function(){
        var that = this;
        wx.request({
            url: app.buildUrl("/member/info"),
            header: app.getRequestHeader(),
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }
                that.setData({
                   user_info:resp.data.info
                });
            }
        });
    },
    showModal(){
        this.setData({
            visible:true
        })
    },
    handleOk() {
        var that = this;
        if (!this.data.index) {
            app.alert({ 'content': '请选择所在的社区~~' });
        } else {
            var member_id = app.getCache('member').member_id
            var platform_id = app.getCache('member').platform_id
            var new_community_id = this.data.communities[this.data.index].community_id
            var new_community_name = this.data.communities[this.data.index].community_name

            wx.request({
                url: app.buildUrl('/member/change-community'),
                header: app.getRequestHeader(),
                method: 'POST',
                data: {
                    member_id:member_id,
                    platform_id: platform_id,
                    community_id: new_community_id,
                    community_name: new_community_name
                },
                success: function (res) {
                    if (res.data.code != 200) {
                        app.alert({ 'content': res.data.msg });
                        return;
                    }

                    that.setData({
                        community_name: new_community_name
                    })
                    var community = {
                        'community_id': new_community_id,
                        'community_name': new_community_name
                    }
                    app.setCache('community', community)
                    that.setData({
                        visible: false
                    })
                }
            });          
        }
    },
    handleClose() {
        this.setData({
            visible: false
        });
    },
    bindPickerChange: function (e) {
        console.log('picker发送选择改变，携带值为', e.detail.value)
        this.setData({
            index: e.detail.value
        })
    },
    getCommunities: function () {
        var that = this
        var platform = app.getCache('platform')
        wx.request({
            url: app.buildUrl('/member/communities'),
            header: app.getRequestHeader(),
            method: 'POST',
            data: {
                platform_id: platform.platform_id
            },
            success: function (res) {
                if (res.data.code != 200) {
                    app.alert({ 'content': res.data.msg });
                    return;
                }

                that.setData({
                    communities: res.data.data.communities
                })
            }
        });
    }
});