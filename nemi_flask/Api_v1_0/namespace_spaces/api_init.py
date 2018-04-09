from flask_restplus import fields

from ..utills.response_init import ProfileError
from ..utills.flask_plus_profile import NamespaceProfile as Namespace


api = Namespace('spaces', description='空间模块')

bucket_simple = api.model('bucket_simple', {
    'id': fields.Integer(description="桶ID"),
    'name': fields.String(description="桶名")
})

folder_simple = api.model('folder_simple', {
    'id': fields.Integer(description="文件夹ID"),
    'object_name': fields.String(description="文件夹名")
})

space_simple = api.model('space_simple', {
    'id': fields.Integer(description="空间ID"),
    'name': fields.String(description="空间名"),
    'space_type': fields.String(description="空间类型"),
    'root_folder': fields.Nested(model=folder_simple, description="空间根目录"),
    'bucket_kids': fields.Nested(model=bucket_simple, as_list=True, description="空间内的桶")
})

come_out_space_success = api.model('come_out_space_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=space_simple, description="内容数据")
})


@api.errorhandler(ProfileError)
def profile_error(error):
    return {'code': error.code, 'success': False, 'message': error.message}, 400
