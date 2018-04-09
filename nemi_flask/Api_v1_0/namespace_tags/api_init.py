from flask_restplus import fields, reqparse

from ..utills.response_init import ProfileError
from ..utills.flask_plus_profile import NamespaceProfile as Namespace, ArgumentProfile


api = Namespace('tags', description='标签模块')


come_in_tag_create = api.model('come_in_tag_create', {
    'name': fields.String(required=True, description="标签名", min_length=2, max_length=40),
    'file_id': fields.Integer(required=True, description="绑定文件的ID")
})

simple_tag_file = api.model('simple_tag_file', {
    'id': fields.Integer(description="文件ID"),
    'object_name': fields.String(description="文件名"),
    'object_type': fields.String(description="文件类型")
})

come_out_tag_item = api.model('come_out_tag_item', {
    'id': fields.Integer(description="标签ID"),
    'name': fields.String(description="标签名"),
    'files': fields.Nested(model=simple_tag_file, description="标签所绑定的文件", as_list=True)
})

come_out_tag_list_success = api.model('come_out_tag_list_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=come_out_tag_item, description="内容数据", as_list=True)
})

come_out_tag_item_success = api.model('come_out_tag_item_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=come_out_tag_item, description="内容数据")
})

parser_tag = reqparse.RequestParser(argument_class=ArgumentProfile)
parser_tag.add_argument('PageIndex', required=False, type=int, location='args',
                        help='分页的索引, 默认为1.')
parser_tag.add_argument('PageSize', required=False, type=int, choices=(10, 20), location='args',
                        help='分页的大小, 默认为10.')
parser_tag.add_argument('OrderBy', required=False, type=str, location='args',
                        help='排序的字段, 默认为"id"，加"-"表示倒序.')


@api.errorhandler(ProfileError)
def profile_error(error):
    return {'code': error.code, 'success': False, 'message': error.message}, 400
