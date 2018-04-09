from flask_restplus import fields, reqparse

from ..utills.response_init import ProfileError
from ..utills.flask_plus_profile import NamespaceProfile as Namespace, ArgumentProfile

from ..namespace_spaces.api_init import space_simple

api = Namespace('message', description='消息模块')

come_out_message_user = api.model('come_out_message_user', {
    'id': fields.Integer(description="id"),
    'username': fields.String(description="用户名"),
    'nickname': fields.String(description="用户昵称"),
    'img_url': fields.String(description="头像地址")
})

come_out_message = api.model('come_out_message', {
    'user_from': fields.Nested(model=come_out_message_user, description="发信人"),
    'user_to': fields.Nested(model=come_out_message_user, description="收信人"),
    'contant': fields.String(description="内容数据"),
    'checked': fields.Boolean(description="是否已读"),
    'last_login_time': fields.DateTime(description="时间")
})

come_out_message_success = api.model('come_out_message_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=come_out_message, as_list=True, description="内容数据")
})

@api.errorhandler(ProfileError)
def profile_error(error):
    return {'code': error.code, 'success': False, 'message': error.message}, 400
