from flask_restplus import fields, reqparse

from ..utills.response_init import ProfileError
from ..utills.flask_plus_profile import NamespaceProfile as Namespace, ArgumentProfile

from ..namespace_spaces.api_init import space_simple
api = Namespace('users', description='用户模块')


user_simple = api.model('user_simple', {
    'id': fields.Integer(description="用户ID"),
    'username': fields.String(description="用户名"),
    'nickname': fields.String(description="用户昵称"),
    'role': fields.String(description="角色身份")
})

come_in_user_create = api.model('come_in_user_create', {
    'email': fields.String(required=True, description="注册邮箱", min_length=6, max_length=40),
    'password': fields.String(required=True, description="密码", min_length=6, max_length=20),
    'role': fields.String(required=True, description="角色身份")
})

come_in_user_edit = api.model('come_in_user_edit', {
    'nickname': fields.String(required=True, description="用户昵称", min_length=2, max_length=60),
    'role': fields.String(required=True, description="用户身份", min_length=2, max_length=60)
})

come_in_user_class = api.model('come_in_user_class', {
    'school_in': fields.String(required=True, description="学校", min_length=2, max_length=60),
    'college_in': fields.String(required=True, description="学院", min_length=2, max_length=60),
    'class_in': fields.String(required=True, description="班级", min_length=2, max_length=60),
    'nick_call': fields.String(required=True, description="称呼", min_length=2, max_length=60),
})

come_out_user_item = api.model('come_out_user_item', {
    'id': fields.Integer(description="用户ID"),
    'email': fields.String(description="用户邮箱"),
    'username': fields.String(description="用户名"),
    'nickname': fields.String(description="用户昵称"),
    'role': fields.String(description="角色身份"),
    'creator': fields.Nested(model=user_simple, description="创建人"),
    'space_mine': fields.Nested(model=space_simple, as_list=True, description="个人空间"),
    'permission': fields.Integer(description="权限码"),
    'is_active': fields.Boolean(description="是否激活"),
    'is_enable': fields.Boolean(description="是否可用"),
    'join_time': fields.DateTime(description="注册时间"),
    'last_login_time': fields.DateTime(description="上一次登录时间"),
    'last_login_ip': fields.String(description="上一次登录"),
    'disable_time': fields.String(description="禁用时间")
})

come_out_user_list_success = api.model('come_out_user_list_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=come_out_user_item, description="内容数据", as_list=True)
})

come_out_user_item_success = api.model('come_out_user_item_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=come_out_user_item, description="内容数据")
})

come_in_user_email = api.model('come_in_user_email', {
    'email': fields.String(required=True, description="用户邮箱", min_length=6, max_length=60)
})

come_in_user_username = api.model('come_in_user_username', {
    'username': fields.String(required=True, description="用户名", min_length=6, max_length=60)
})

come_in_user_password = api.model('come_in_user_password', {
    'old_password': fields.String(required=True, description="旧密码", min_length=6, max_length=60),
    'new_password': fields.String(required=True, description="新密码", min_length=6, max_length=60)
})

come_in_reset_password = api.model('come_in_reset_password', {
    'password': fields.String(required=True, description="新密码", min_length=6, max_length=60)
})

come_in_user_permission = api.model('come_in_user_permission', {
    'permission': fields.String(required=True, description="权限", min_length=6, max_length=60)
})

parser_username = reqparse.RequestParser(argument_class=ArgumentProfile)
parser_username.add_argument('username', required=True, type=str, location='args',
                             help='替换的用户名。')

parser_email = reqparse.RequestParser(argument_class=ArgumentProfile)
parser_email.add_argument('email', required=True, type=str, location='args',
                          help='替换的邮箱地址。')


@api.errorhandler(ProfileError)
def profile_error(error):
    return {'code': error.code, 'success': False, 'message': error.message}, 400
