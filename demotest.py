# import calendar
# import time
# day_now = time.localtime()
# day_begin = '%d-%02d-01' % (day_now.tm_year, day_now.tm_mon)  # 月初肯定是1号
# wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
# day_end = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)
# print('月初日期为：',day_begin, '月末日期为：',day_end)
#

# MINA_APP = {
#     'appid': 'wxc6fe31db7712ed76',
#     'appkey': '1e51a3a1414b82c02836af67d5567fe7',
#     'paykey': 'R4WLnVMepFlfgjFHXCbuYfJ2UJ1lyoQx',
#     'mch_id': '1357377302',
#     'callback_url': '/api/order/callback',
#     'boao': {
#         'appid': 'wx26044e0f3a608e45',
#         'appkey': '51c34d1cfb2bc56b0748a2be570f06e9',
#         'paykey': 'R4WLnVMepFlfgjFHXCbuYfJ2UJ1lyoQx',
#         'mch_id': '1357377302',
#         'callback_url': '/api/order/callback',
#     },
# }
#
# boao = 'boao'
# print(MINA_APP[boao])
