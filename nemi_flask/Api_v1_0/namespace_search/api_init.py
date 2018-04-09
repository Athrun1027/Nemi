from flask_restplus import fields, reqparse

from ..utills.response_init import ProfileError
from ..utills.flask_plus_profile import NamespaceProfile as Namespace, ArgumentProfile


api = Namespace('search', description='搜索模块')

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


come_out_search_item = api.model('come_out_search_item', {
    'id': fields.Integer(description="文件ID"),
    'object_name': fields.String(description="文件名"),
    'object_type': fields.String(description="文件类型"),
    'object_size': fields.Integer(description="文件大小"),
    'object_uuid': fields.String(description="文件UUID"),
    'join_time': fields.DateTime(description="创建时间"),
    'edit_time': fields.DateTime(description="修改时间")
})

come_out_search_list_success = api.model('come_out_search_list_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=come_out_search_item, description="内容数据", as_list=True)
})

parser_search = reqparse.RequestParser(argument_class=ArgumentProfile)
parser_search.add_argument('PageIndex', required=False, type=int, location='args',
                           help='分页的索引, 默认为1.')
parser_search.add_argument('PageSize', required=False, type=int, choices=(10, 20), location='args',
                           help='分页的大小, 默认为10.')
parser_search.add_argument('OrderBy', required=False, type=str, location='args',
                           help='排序的字段, 默认为"id"，加"-"表示倒序.')
parser_search.add_argument('Search', required=True, type=str, location='args',
                           help='搜索关键字')
parser_search.add_argument('Type', required=False, type=str, location='args',
                           help='搜索类型')


@api.errorhandler(ProfileError)
def profile_error(error):
    return {'code': error.code, 'success': False, 'message': error.message}, 400
