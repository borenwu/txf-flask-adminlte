# -*- coding: utf-8 -*-
SERVER_PORT = 5000
DEBUG = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@47.96.148.158/food_db?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf8mb4"

# 有可能你使用浏览器看到的一串字符串不是那么容易看懂的，这是因为python底层使用unicode编码。
# 通过设置下面的参数可以解决这个问题。
JSON_AS_ASCII = False

AUTH_COOKIE_NAME = "mooc_food"

SEO_TITLE = "淘鲜蜂社区拼团"
##过滤url
IGNORE_URLS = [
    "^/user/login"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

API_IGNORE_URLS = [
    "^/api"
]

PAGE_SIZE = 50
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "1": "正常",
    "0": "已删除"
}

MINA_APP = {
    'appid': 'wxc6fe31db7712ed76',
    'appkey': '1e51a3a1414b82c02836af67d5567fe7',
    'paykey': 'R4WLnVMepFlfgjFHXCbuYfJ2UJ1lyoQx',
    'mch_id': '1357377302',
    'callback_url': '/api/order/callback',
    'boao': {
        'appid': 'wx26044e0f3a608e45',
        'appkey': '51c34d1cfb2bc56b0748a2be570f06e9',
        'paykey': 'R4WLn6MepFlfgjFHXC9uYfJ2UJ1lyoBr',
        'mch_id': '1516259371',
        'callback_url': '/api/order/callback',
    },
}

UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}

APP = {
    'domain': 'https://ntboao.net'
}

PAY_STATUS_MAPPING = {
    "1": "已支付",
    "-8": "待支付",
    "0": "已关闭"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0": "订单关闭",
    "1": "支付成功",
    "-8": "待支付",
    "-7": "待发货",
    "-6": "待确认",
    "-5": "待评价"
}

QINIU_ACCESS_KEY = 'rsnQ1mPiWJwthOmbSSIfwvsKkNX0ZzTrISaLMlM0'
QINIU_SECRET_KEY = 'Gu00U4X8-KUgHIAybg4TeeZnhjRX5d7-Dn8Jo89M'
QINIU_BUCKET_NAME = 'ntboao'
QINIU_BUCKET_DOMAIN = 'http://oy98650kl.bkt.clouddn.com'
