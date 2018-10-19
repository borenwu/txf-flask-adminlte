//login.js
//获取应用实例
var app = getApp();
Page({
    data: {
        visible: false,
        remind: '加载中',
        angle: 0,
        userInfo: {},
        regFlag: true,
        communities: []
    },
    handleOk() {
        if (!this.data.index) {
            app.alert({
                'content': '请选择所在的社区~~'
            });
        } else {
            var community_id = this.data.communities[this.data.index].community_id
            var community_name = this.data.communities[this.data.index].community_name
            var community = {
                'community_id': community_id,
                'community_name': community_name
            }
            app.setCache('community', community)
            this.setData({
                visible: false
            })
        }
    },
    handleClose() {
        app.alert({
            'content': '请选择所在的社区~~'
        });
    },
    bindPickerChange: function(e) {
        console.log('picker发送选择改变，携带值为', e.detail.value)
        this.setData({
            index: e.detail.value
        })
    },
    goToIndex: function() {
        wx.switchTab({
            url: '/pages/food/index',
        });
    },
    onLoad: function() {
        this.getCommunities();
        this.checkLogin();


        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });

    },
    onShow: function() {

    },
    onReady: function() {
        var that = this;
        setTimeout(function() {
            that.setData({
                remind: ''
            });
        }, 1000);
        wx.onAccelerometerChange(function(res) {
            var angle = -(res.x * 30).toFixed(1);
            if (angle > 14) {
                angle = 14;
            } else if (angle < -14) {
                angle = -14;
            }
            if (that.data.angle !== angle) {
                that.setData({
                    angle: angle
                });
            }
        });
    },
    checkLogin: function() {
        var that = this;
        wx.login({
            success: function(res) {
                if (!res.code) {
                    app.alert({
                        'content': '登录失败，请再次点击~~'
                    });
                    return;
                }
                wx.request({
                    url: app.buildUrl('/member/check-reg'),
                    header: app.getRequestHeader(),
                    method: 'POST',
                    data: {
                        code: res.code
                    },
                    success: function(res) {
                        if (res.data.code != 200) {
                            that.setData({
                                visible: true
                            })

                            that.setData({
                                regFlag: false
                            });
                            return;
                        }
                        var member_info = {
                            platform_id: res.data.data.platform_id,
                            member_id: res.data.data.member_id
                        }
                        var community = {
                            'community_id': res.data.data.community_id,
                            'community_name': res.data.data.community_name
                        }
                        app.setCache('community', community)
                        app.setCache("token", res.data.data.token);
                        app.setCache("member", member_info);
                        //that.goToIndex();
                    }
                });
            }
        });
    },
    login: function(e) {
        var that = this;
        if (!e.detail.userInfo) {
            app.alert({
                'content': '登录失败，请再次点击~~'
            });
            return;
        }

        var data = e.detail.userInfo;
        var community_id = app.getCache('community').community_id;
        var community_name = app.getCache('community').community_name;
        var platform_id = app.getCache('platform').platform_id;
        wx.login({
            success: function(res) {
                if (!res.code) {
                    app.alert({
                        'content': '登录失败，请再次点击~~'
                    });
                    return;
                }
                data['code'] = res.code;
                data['platform_id'] = platform_id
                data['community_id'] = community_id
                data['community_name'] = community_name
                wx.request({
                    url: app.buildUrl('/member/login'),
                    header: app.getRequestHeader(),
                    method: 'POST',
                    data: data,
                    success: function(res) {
                        if (res.data.code != 200) {
                            app.alert({
                                'content': res.data.msg
                            });
                            return;
                        }
                        var member_info = {
                            platform_id: res.data.data.platform_id,
                            member_id: res.data.data.id
                        }
                        app.setCache("token", res.data.data.token);
                        app.setCache("member", member_info);
                        that.goToIndex();
                    }
                });
            }
        });
    },
    getCommunities: function() {
        var that = this
        var platform = app.getCache('platform')
        wx.request({
            url: app.buildUrl('/member/communities'),
            header: app.getRequestHeader(),
            method: 'POST',
            data: {
                platform_id: platform.platform_id
            },
            success: function(res) {
                if (res.data.code != 200) {
                    app.alert({
                        'content': res.data.msg
                    });
                    return;
                }

                that.setData({
                    communities: res.data.data.communities
                })
            }
        });
    }
});