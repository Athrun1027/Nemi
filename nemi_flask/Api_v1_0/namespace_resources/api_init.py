from flask_restplus import fields, reqparse

from ..utills.response_init import ProfileError
from ..utills.flask_plus_profile import NamespaceProfile as Namespace, ArgumentProfile


api = Namespace('resources', description='资源模块')

user_simple = api.model('user_simple', {
    'id': fields.Integer(description="用户ID"),
    'username': fields.String(description="用户名"),
    'nickname': fields.String(description="用户昵称"),
    'role': fields.String(description="角色身份")
})

bucket_simple = api.model('bucket_simple', {
    'id': fields.Integer(description="桶ID"),
    'name': fields.String(description="桶名")
})

folder_simple = api.model('folder_simple', {
    'id': fields.Integer(description="文件夹ID"),
    'object_name': fields.String(description="文件夹名")
})

tag_simple = api.model('tag_simple', {
    'id': fields.Integer(description="标签ID"),
    'name': fields.String(description="标签名")
})

share_files_simple = api.model('share_files_simple', {
    'id': fields.Integer(description="分享ID"),
    'name': fields.String(description="文件名"),
    'own_id': fields.Integer(description="用户id")
})

file_all = api.model('file_all', {
    'id': fields.Integer(description="文件ID"),
    'object_name': fields.String(description="文件名"),
    'object_type': fields.String(description="文件类型"),
    'object_size': fields.Integer(description="文件大小"),
    'object_uuid': fields.String(description="文件UUID"),
    'folder': fields.Nested(model=folder_simple, description="所属文件夹"),
    'creator': fields.Nested(model=user_simple, description="创建人"),
    'bucket': fields.Nested(model=bucket_simple, description="所属桶"),
    'tags': fields.Nested(model=tag_simple, description="所有标签", as_list=True),
    'share_files': fields.Nested(model=share_files_simple, description="所有标签", as_list=True),
    'join_time': fields.DateTime(description="创建时间"),
    'open_time': fields.DateTime(description="开放时间"),
    'edit_time': fields.DateTime(description="修改时间")
})

come_out_resource_list_success = api.model('come_out_resource_list_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=file_all, description="内容数据", as_list=True)
})

come_out_resource_item_success = api.model('come_out_resource_item_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=file_all, description="内容数据", as_list=True)
})

come_in_file_edit = api.model('come_in_file_edit', {
    'object_name': fields.String(description="文件名", min_length=2, max_length=60)
})

come_in_file_move = api.model('come_in_file_move', {
    'folder_id': fields.Integer(description="文件名", min_length=2, max_length=60)
})

parser = reqparse.RequestParser(argument_class=ArgumentProfile)
parser.add_argument('PageIndex', required=False, type=int, location='args',
                    help='分页的索引, 默认为1.')
parser.add_argument('PageSize', required=False, type=int, choices=(10, 20, 50), location='args',
                    help='分页的大小, 默认为10.')
parser.add_argument('OrderBy', required=False, type=str, location='args',
                    help='排序的字段, 默认为"id"，加"-"表示倒序.')
parser.add_argument('Disable', required=False, type=int, location='args',
                    help='是否查询禁用的对象, 默认为否，若是填写1.')
parser.add_argument('folder_id', required=False, type=int, location='args',
                    help='是否查询禁用的对象, 默认为否，若是填写1.')


@api.errorhandler(ProfileError)
def profile_error(error):
    return {'code': error.code, 'success': False, 'message': error.message}, 400
