from models import db, File, Tag
from flask import g, request

from ..utills.nemi_framework import ResourceList, ResourceCreate
from ..utills.wraps_define import login_require

from ..utills.response_init import success_response
from flask_restplus import Resource

from .api_init import api, come_out_search_list_success


@api.route('/')
@api.response(400, '参数形式有误')
class SearchList(Resource):

    @api.marshal_with(come_out_search_list_success, code=200, description="成功列出搜索结果!")
    @login_require
    def put(self):
        """列出搜索结果"""
        search_text = request.json.get("search_text")
        search_file_type = request.json.get("search_file_type")
        search_space = request.json.get("search_space")
        instances = []
        if search_space == "user":
            instances = File.query.filter(File.bucket_id == g.login_user.space_mine[0].bucket_kids[0].id,
                                          File.is_enable == True,
                                          File.folder_id != None,
                                          File.object_name.contains(search_text))
            if search_file_type == "pdf":
                instances = instances.filter(File.object_type == "pdf")
            if search_file_type == "jpg":
                instances = instances.filter(File.object_type.in_(['jpg', 'jpeg', 'png']))
            if search_file_type == "markdown":
                instances = instances.filter(File.object_type == "markdown")
            instances = instances.all()
        else:
            instances_temp = []
            for item in g.login_user.groups:
                for item_bucket in item.space_mine[0].bucket_kids:
                    instances_temp += item_bucket.file_in
            for item in instances_temp:
                if (search_text in item.object_name) and (item.is_enable == True) and (
                    item.folder_id != None
                ):
                    if search_file_type == "pdf" and item.object_type == "pdf":
                        instances.append(item)
                    if search_file_type == "jpg" and item.object_type in ["jpg", "jpeg", "png"]:
                        instances.append(item)
                    if search_file_type == "markdown" and item.object_type == "markdown":
                        instances.append(item)
                    if search_file_type == "all":
                        instances.append(item)
        return success_response(data=instances)

