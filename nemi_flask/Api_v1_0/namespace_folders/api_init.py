from flask_restplus import fields

from ..utills.response_init import ProfileError
from ..utills.flask_plus_profile import NamespaceProfile as Namespace


api = Namespace('folders', description='目录模块')

folder_simple = api.model('folder_simple', {
    'id': fields.Integer(description="文件夹ID"),
    'object_name': fields.String(description="文件夹名")
})

come_out_folder_success = api.model('come_out_folder_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=folder_simple, description="内容数据")
})

come_in_folder_create = api.model('come_in_folder_create', {
    'object_name': fields.String(required=True, description="目录名称", min_length=2, max_length=60),
    'folder_id': fields.Integer(required=True, description="目录ID")
})


@api.errorhandler(ProfileError)
def profile_error(error):
    return {'code': error.code, 'success': False, 'message': error.message}, 400
