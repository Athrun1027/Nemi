from flask_restplus import fields, reqparse

from ..utills.response_init import ProfileError
from ..utills.flask_plus_profile import NamespaceProfile as Namespace, ArgumentProfile

from ..namespace_spaces.api_init import space_simple
api = Namespace('groups', description='群组模块')


group_user_simple = api.model('group_user_simple', {
    'id': fields.Integer(description="用户ID"),
    'username': fields.String(description="用户名"),
    'nickname': fields.String(description="用户昵称"),
    'role': fields.String(description="角色身份")
})

come_in_group_create = api.model('come_in_group_create', {
    'name': fields.String(required=True, description="群组名", min_length=2, max_length=40)
})

come_in_group_edit = api.model('come_in_group_edit', {
    'nickname': fields.String(required=True, description="用户昵称", min_length=2, max_length=60)
})

come_out_group_item = api.model('come_out_group_item', {
    'id': fields.Integer(description="用户ID"),
    'name': fields.String(description="群组名"),
    'nickname': fields.String(description="群组昵称"),
    'creator': fields.Nested(model=group_user_simple, description="创建人"),
    'space_mine': fields.Nested(model=space_simple, as_list=True, description="群组空间"),
    'permission': fields.Integer(description="权限码"),
    'is_enable': fields.Boolean(description="是否可用"),
    'join_time': fields.DateTime(description="创建时间"),
    'disable_time': fields.String(description="禁用时间")
})

come_out_group_list_success = api.model('come_out_group_list_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=come_out_group_item, description="内容数据", as_list=True)
})

come_out_group_item_success = api.model('come_out_group_item_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=come_out_group_item, description="内容数据")
})

come_in_group_nickname = api.model('come_in_group_nickname', {
    'nickname': fields.String(required=True, description="用户名", min_length=6, max_length=60)
})

come_in_group_permission = api.model('come_in_group_permission', {
    'permission': fields.String(required=True, description="权限", min_length=6, max_length=60)
})

parser_group_name = reqparse.RequestParser(argument_class=ArgumentProfile)
parser_group_name.add_argument('username', required=True, type=str, location='args',
                               help='替换的用户名。')

parser_group_email = reqparse.RequestParser(argument_class=ArgumentProfile)
parser_group_email.add_argument('email', required=True, type=str, location='args',
                                help='替换的邮箱地址。')


@api.errorhandler(ProfileError)
def profile_error(error):
    return {'code': error.code, 'success': False, 'message': error.message}, 400
