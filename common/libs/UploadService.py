# -*- coding: utf-8 -*-
from werkzeug.utils import secure_filename
from application import app, db,qiniu_store
from common.libs.Helper import getCurrentDate
import datetime
import os, stat, uuid
from common.models.Image import Image


# access_key = 'rsnQ1mPiWJwthOmbSSIfwvsKkNX0ZzTrISaLMlM0'
# secret_key = 'Gu00U4X8-KUgHIAybg4TeeZnhjRX5d7-Dn8Jo89M'

#构建鉴权对象
# q = Auth(access_key, secret_key)
#要上传的空间
# bucket_name = 'Bucket_Name'
# token = q.upload_token(bucket_name, 3600)



class UploadService():
    @staticmethod
    def uploadByFile(file):
        config_upload = app.config['UPLOAD']
        resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
        filename = file.filename
        ext = filename.rsplit(".", 1)[1]
        if ext not in config_upload['ext']:
            resp['code'] = -1
            resp['msg'] = "不允许的扩展类型文件"
            return resp

        root_path = app.root_path + config_upload['prefix_path']
        # 不使用getCurrentDate创建目录，为了保证其他写的可以用，这里改掉，服务器上好像对时间不兼容
        file_dir = "http://oy98650kl.bkt.clouddn.com"
        # save_dir = root_path + file_dir
        # if not os.path.exists(save_dir):
        #     os.mkdir(save_dir)
        #     os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)

        # print(file.read())
        # file_name = str(uuid.uuid4()).replace("-", "") + "." + ext

        result = qiniu_store.save(file.read(), filename)
        # print(result)
        # print(info)

        # file.save("{0}/{1}".format(save_dir, file_name))

        model_image = Image()
        model_image.file_key = file_dir + "/" + filename
        model_image.created_time = getCurrentDate()
        db.session.add(model_image)
        db.session.commit()

        resp['data'] = {
            'file_key': model_image.file_key
        }
        return resp
