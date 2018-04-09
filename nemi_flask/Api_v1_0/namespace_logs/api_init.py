from flask_restplus import fields, reqparse

from ..utills.response_init import ProfileError
from ..utills.flask_plus_profile import NamespaceProfile as Namespace, ArgumentProfile


api = Namespace('logs', description='日志模块')


request_user_create = api.model('request_user_create', {
    'email': fields.String(required=True, description="注册邮箱", min_length=6, max_length=40),
    'password': fields.String(required=True, description="密码", min_length=6, max_length=20),
    'role': fields.String(required=True, description="角色身份")
})

request_user_nickname = api.model('request_user_nickname', {
    'nickname': fields.String(required=True, description="用户昵称", min_length=6, max_length=60)
})

request_user_email = api.model('request_user_email', {
    'email': fields.String(required=True, description="用户邮箱", min_length=6, max_length=60)
})

request_user_username = api.model('request_user_username', {
    'username': fields.String(required=True, description="用户名", min_length=6, max_length=60)
})

request_user_password = api.model('request_user_password', {
    'old_password': fields.String(required=True, description="旧密码", min_length=6, max_length=60),
    'new_password': fields.String(required=True, description="新密码", min_length=6, max_length=60)
})

request_user_permission = api.model('request_user_permission', {
    'permission': fields.String(required=True, description="权限", min_length=6, max_length=60)
})

response_user_simple = api.model('response_user_simple', {
    'id': fields.Integer(description="用户ID"),
    'username': fields.String(description="用户名"),
    'nickname': fields.String(description="用户昵称"),
    'role': fields.String(description="角色身份")
})

response_user_item = api.model('response_user_item', {
    'id': fields.Integer(description="用户ID"),
    'email': fields.String(description="用户邮箱"),
    'username': fields.String(description="用户名"),
    'nickname': fields.String(description="用户昵称"),
    'role': fields.String(description="角色身份"),
    'creator': fields.Nested(model=response_user_simple, description="创建人"),
    'permission': fields.Integer(description="权限码"),
    'is_active': fields.Boolean(description="是否激活"),
    'is_enable': fields.Boolean(description="是否可用"),
    'join_time': fields.DateTime(description="注册时间"),
    'last_login_time': fields.DateTime(description="上一次登录时间"),
    'last_login_ip': fields.String(description="上一次登录"),
    'disable_time': fields.String(description="禁用时间")
})

response_user_list_success = api.model('response_user_list_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=response_user_item, description="内容数据", as_list=True)
})

response_user_item_success = api.model('response_user_item_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=response_user_item, description="内容数据")
})

response_success_message = api.model('response_success_message', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.String(description="内容数据")
})


parser = reqparse.RequestParser(argument_class=ArgumentProfile)
parser.add_argument('PageIndex', required=False, type=int, location='args',
                    help='分页的索引, 默认为1.')
parser.add_argument('PageSize', required=False, type=int, choices=(10, 20), location='args',
                    help='分页的大小, 默认为10.')
parser.add_argument('OrderBy', required=False, type=str, location='args',
                    help='排序的字段, 默认为"id"，加"-"表示倒序.')
parser.add_argument('Disable', required=False, type=int, location='args',
                    help='是否查询禁用的用户, 默认为否，若是填写1.')
# parser.add_argument('Nemi-API-KEY', required=False, location='headers',
#                     help='用户认证的Token, 例: "Nemi xxxxx"')

parser_username = reqparse.RequestParser(argument_class=ArgumentProfile)
parser_username.add_argument('username', required=True, type=str, location='args',
                             help='替换的用户名。')

parser_email = reqparse.RequestParser(argument_class=ArgumentProfile)
parser_email.add_argument('email', required=True, type=str, location='args',
                          help='替换的邮箱地址。')


@api.errorhandler(ProfileError)
def profile_error(error):
    return {'code': error.code, 'success': False, 'message': error.message}, 400
