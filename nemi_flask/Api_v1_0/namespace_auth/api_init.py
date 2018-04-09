from flask_restplus import fields, reqparse

from ..utills.flask_plus_profile import NamespaceProfile as Namespace, ArgumentProfile

from ..namespace_spaces.api_init import space_simple

api = Namespace('auth', description='认证模块(完成)')


come_in_login = api.model('come_in_login', {
    'username': fields.String(required=True, description="用户名或密码", min_length=6, max_length=40),
    'password': fields.String(required=True, description="密码", min_length=6, max_length=20)
})

token = api.model('token', {
    'token': fields.String(description="认证成功后的令牌")
})

come_out_success = api.model('come_out_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.String(description="内容数据")
})

come_out_token_success = api.model('come_out_token_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=token, description="内容数据")
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

error_message = api.model('error_message', {
    'username': fields.String(required=True, description="用户名或密码", min_length=6, max_length=40),
    'password': fields.String(required=True, description="密码", min_length=6, max_length=20)
})

user_simple_auth = api.model('user_simple_auth', {
    'id': fields.Integer(description="空间ID"),
    'username': fields.String(description="空间名"),
    'nickname': fields.String(description="空间类型")
})

come_out_login_contant = api.model('come_out_login_contant', {
    'id': fields.Integer(description="用户ID"),
    'email': fields.String(description="用户邮箱"),
    'username': fields.String(description="用户名"),
    'nickname': fields.String(description="用户昵称"),
    'role': fields.String(description="角色身份"),
    'school_in': fields.String(description="所在学校"),
    'college_in': fields.String(description="所在学院"),
    'class_in': fields.String(description="所在班级"),
    'nick_call': fields.String(description="称呼"),
    'img_url': fields.String(description="头像地址"),
    'buckets_count': fields.Integer(description="桶个数"),
    'files_count': fields.Integer(description="文件个数"),
    'files_size': fields.Integer(description="文件大小"),
    'is_changed': fields.Boolean(description="是否已经修改用户名"),
    'space_mine': fields.Nested(model=space_simple, as_list=True, description="个人空间"),
    'kids': fields.Nested(model=user_simple_auth, as_list=True, description="子用户"),
    'files_types': fields.Raw(description="文件分类"),
    'last_login_time': fields.DateTime(description="上一次登录时间"),
    'last_login_ip': fields.String(description="上一次登录")
})

come_out_user_login = api.model('come_out_user_login', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=come_out_login_contant, description="内容数据")
})