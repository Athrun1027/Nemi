from flask import g

from models import User, db, Space, Bucket, File, Message

from ..utills.nemi_framework import ResourceList, ResourceCreate
from ..utills.nemi_framework import ResourceItem, ResourceEdit, ResourceDelete
from ..utills.nemi_framework import ResourceHit, ResourceValidate

from ..utills.response_init import ProfileError
from ..utills.wraps_define import login_require
from ..utills.response_init import success_response


from ..namespace_auth.api_init import parser, come_out_success
from .api_init import api, come_out_message_success


@api.route('/recent')
@api.response(400, '参数形式有误')
class MessageList(ResourceList):
    list_parser = parser
    model = Message
    db = db

    @api.marshal_with(come_out_message_success, code=200, description="成功列出消息列表!")
    @login_require
    def get(self):
        """列出消息列表"""
        # 得到符合条件的对象列表
        instances = self.model.query.filter(self.model.user_to_id == g.login_user.id).order_by(self.model.last_login_time.desc()).all()[:6]
        return success_response(data=instances)

@api.route('/checked')
@api.response(400, '参数形式有误')
class MessageList(ResourceList):
    list_parser = parser
    model = Message
    db = db

    @api.marshal_with(come_out_message_success, code=200, description="成功列出消息列表!")
    @login_require
    def get(self):
        """列出消息列表"""
        # 得到符合条件的对象列表
        instances = self.model.query.filter(self.model.user_to_id == g.login_user.id, self.model.checked == False).order_by(self.model.last_login_time.desc()).all()
        return success_response(data=instances)
