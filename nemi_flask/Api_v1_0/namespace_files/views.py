from flask import g, request, stream_with_context, Response
from flask_restplus import Resource
from models import db, File
import os
import uuid

from ..utills.nemi_framework import ResourceCreate, ResourceItem

from ..utills.wraps_define import login_require
from ..utills.response_init import success_response

from .api_init import api, come_out_test_success, come_out_file_success
from ..namespace_resources.api_init import come_out_resource_list_success

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
upload_dir = BASE_DIR + "/upload/"


@api.route('/')
@api.response(400, '参数形式有误')
class FileCreate(ResourceCreate):
    model = File
    db = db

    @login_require
    def post(self):
        """上传文件"""
        folder_id = request.form.get("folder_id")
        bucket_id = request.form.get("bucket_id")
        for item in request.files:
            item_file = request.files.get(item)
            item_file.save("./upload/"+item_file.filename)
            item_file_size = request.form.get(item + "_size")
            file_object_save(item_file, folder_id, item_file_size, bucket_id)
        return {"status": "success"}


def generate(filename):
    with open("./upload/"+filename, "rb+") as r:
        while True:
            chunk_data = r.read(512)
            if not chunk_data:
                break
            yield chunk_data


@api.route('/download/<int:pk>')
@api.response(400, '参数形式有误')
class FileDownload(ResourceItem):
    model = File
    db = db

    def get(self, pk):
        """下载文件"""
        instance = self.get_instance(pk)
        if instance.object_uuid is None:
            return "不给你下载"
        file_name = instance.object_name.encode().decode('latin-1')
        response = Response(stream_with_context(generate(instance.object_name)))
        response.headers['Content-Disposition'] = "attachment; filename={0}".format(file_name)
        response.headers['Content-Type'] = "application/octet-stream"
        response.headers['Content-Length'] = instance.object_size
        return response


def file_object_save(item_file, folder_id, item_file_size, bucket_id):
    create_body = dict()
    create_body["object_name"] = item_file.filename
    create_body["object_type"] = item_file.content_type.split("/")[-1]
    create_body["object_size"] = item_file_size
    create_body["object_uuid"] = str(uuid.uuid1())
    create_body["creator_id"] = g.login_user.id
    create_body["folder_id"] = folder_id
    create_body["bucket_id"] = bucket_id
    file_object = File(**create_body)
    db.session.add(file_object)
    db.session.commit()
    # TODO 根据uuid在对象存储创建对象
    return file_object


@api.route('/recent/')
@api.response(400, '参数形式有误')
class FolderRecent(Resource):
    model = File
    db = db

    @api.marshal_with(come_out_resource_list_success, code=201, description="成功获取最近的文件!")
    @login_require
    def get(self):
        """最近的文件"""
        instances = self.model.query.filter(self.model.is_enable == True, self.model.object_type != "folder", self.model.creator_id == g.login_user.id).order_by(self.model.edit_time.desc()).all()[:12]
        return success_response(data=instances)
