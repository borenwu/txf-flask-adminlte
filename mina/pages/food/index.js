//index.js
//获取应用实例
var app = getApp();
Page({
    data: {
        indicatorDots: true,
        autoplay: true,
        interval: 3000,
        duration: 1000,
        loadingHidden: false, // loading
        swiperCurrent: 0,
        categories: [],
        activeCategoryId: 0,
        goods: [],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        p:1,
        // processing:false
    },
    onPullDownRefresh:function() {
        this.getBannerAndCat();
        // this.getFoodList();
    },
    onLoad: function () {
        wx.showShareMenu({
            withShareTicket: true //要求小程序返回分享目标信息
        })
        var that = this;
        
    },
    onShareAppMessage() {
        return {
            title: '分享这个小程序',
            path: '/pages/index/index',
        }
    },
    //解决切换不刷新维内托，每次展示都会调用这个方法
    onShow:function(){
        var community_name = app.getCache('community').community_name
        wx.setNavigationBarTitle({
            title: community_name + '-最近开团新品'
        });
        this.getBannerAndCat();
    },
    scroll: function (e) {
        var that = this, scrollTop = that.data.scrollTop;
        that.setData({
            scrollTop: e.detail.scrollTop
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
    listenerSearchInput:function( e ){
        this.setData({
            searchInput: e.detail.value
        });
    },
    toSearch:function( e ){
        this.setData({
            p:1,
            goods:[],
            loadingMoreHidden:true
        });
        this.getFoodList();
	},
    tapBanner: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
                url: "/pages/food/info?id=" + e.currentTarget.dataset.id
            });
        }
    },
    toDetailsTap: function (e) {
        var food_id = e.currentTarget.dataset.id
        var member_id = app.getCache('member').member_id

        wx.request({
            url: app.buildUrl("/member/check-limit"),
            header: app.getRequestHeader(),
            data: {
                food_id: food_id,
                member_id: member_id
            },
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({ "content": resp.msg });
                    return;
                }
                wx.navigateTo({
                    url: "/pages/food/info?id=" + e.currentTarget.dataset.id
                });
            }
        });

    },
    getBannerAndCat: function () {
        console.log('get banner and cat')
        var that = this;
        var platform = app.getCache('platform')
        var community_name = app.getCache('community').community_name
        wx.request({
            url: app.buildUrl("/food/index"),
            data: {
                platform_id:platform.platform_id,
                community_name: community_name
            },
            header: app.getRequestHeader(),
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }

                that.setData({
                    banners: resp.data.banner_list,
                    categories: resp.data.cat_list
                });
                that.getFoodList();
            }
        });
    },
    catClick: function (e) {
        this.setData({
            activeCategoryId: e.currentTarget.id
        });
        this.setData({
            loadingMoreHidden: true,
            p:1,
            goods:[]
        });
        this.getFoodList();
    },
    // onReachBottom: function () {
    //     var that = this;
    //     setTimeout(function () {
    //         that.getFoodList();
    //     }, 500);
    // },
    getFoodList: function () {
        console.log('get food list')
        var that = this;
        // if( that.data.processing ){
        //     return;
        // }

        // if( !that.data.loadingMoreHidden ){
        //     return;
        // }

        // that.setData({
        //     processing:true
        // });

        var platform = app.getCache('platform')
        var community_name = app.getCache('community').community_name
        wx.request({
            url: app.buildUrl("/food/search"),
            header: app.getRequestHeader(),
            data: {
                platform_id: platform.platform_id,
                community_name:community_name,
                cat_id: that.data.activeCategoryId,
                mix_kw: that.data.searchInput,
                p: that.data.p,
            },
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }

                var goods = resp.data.list;
                for(var i =0 ; i<goods.length;i++){
                    if(goods[i].stock == 0){
                        goods[i].isEmpty = true
                    }else{
                        goods[i].isEmpty = false
                    }
                }
                that.setData({
                    goods:  goods,
                    p: that.data.p + 1,
                    // processing:false
                });

                if( resp.data.has_more == 0 ){
                    that.setData({
                        loadingMoreHidden: false
                    });
                }

            }
        });
    }
});
