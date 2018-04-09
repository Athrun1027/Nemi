from werkzeug.datastructures import FileStorage
from flask_restplus import fields, reqparse


from ..utills.response_init import ProfileError
from ..utills.flask_plus_profile import NamespaceProfile as Namespace, ArgumentProfile


api = Namespace('files', description='文件模块')

file_simple = api.model('file_simple', {
    'id': fields.Integer(description="文件ID"),
    'object_name': fields.String(description="文件名"),
    'object_type': fields.String(description="文件类型"),
    'object_size': fields.Integer(description="文件大小"),
    'object_uuid': fields.String(description="文件UUID")
})

come_out_file_success = api.model('come_out_file_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=file_simple, description="内容数据")
})

come_out_test_success = api.model('come_out_file_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.String(description="内容数据")
})


@api.errorhandler(ProfileError)
def profile_error(error):
    return {'code': error.code, 'success': False, 'message': error.message}, 400
