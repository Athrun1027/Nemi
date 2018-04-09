from flask import g
from sqlalchemy import or_
from datetime import datetime

from models import User, db

from ..utills.framework_profile import ResourceList, ResourceItem, ResourceEnable, ResourcePerform, ResourceValidate
from ..utills.response_init import ProfileError
from ..utills.wraps_define import login_require

from ..namespace_auth.api_init import error_message

from .api_init import api, request_user_create, parser, parser_username
from .api_init import response_user_item_success, response_user_list_success
from .api_init import request_user_nickname, request_user_email
from .api_init import response_success_message
from .api_init import parser_email, request_user_username
from .api_init import request_user_permission, request_user_password


@api.route('/')
@api.response(400, '参数形式有误', error_message)
class UserList(ResourceList):
    list_parser = parser
    model = User
    db = db

    @api.marshal_with(response_user_list_success, code=200, description="成功列出用户列表!")
    @api.expect(parser)
    def get(self):
        """列出用户列表"""
        return super(UserList, self).get()

    @api.marshal_with(response_user_item_success, code=201, description="成功创建用户对象!")
    @api.expect(request_user_create)
    @login_require
    def post(self):
        """创建用户对象"""
        return super(UserList, self).post()

    def get_instances(self, is_disable, order_object, page_index, page_size):
        instances = self.model.query.filter(self.model.is_enable != is_disable).order_by(order_object) \
            .paginate(page=page_index, per_page=page_size, error_out=False)
        return instances

    def create_instance(self, body_data):
        instance_exist = self.db.session.query(self.model).filter(or_(
            self.model.username == body_data["email"], self.model.email == body_data["email"])).first()
        if instance_exist is not None:
            raise ProfileError(code=400, message={
                "email": "This email is already exist!"
            })
        instance = self.model(email=body_data["email"],
                              role=body_data["role"],
                              creator_id=g.login_user.id)
        instance.set_password(body_data["password"])
        return instance


@api.route('/<int:pk>')
@api.param('pk', '需要查找的用户ID')
@api.response(400, '参数形式有误', error_message)
class UserItem(ResourceItem):
    model = User
    db = db

    @api.marshal_with(response_user_item_success, code=200, description="成功获取用户对象!")
    @login_require
    def get(self, pk):
        """获取用户对象"""
        return super(UserItem, self).get(pk)

    @api.marshal_with(response_user_item_success, code=200, description="成功修改用户对象信息!")
    @api.expect(request_user_nickname)
    @login_require
    def put(self, pk):
        """修改用户对象信息"""
        return super(UserItem, self).put(pk)

    @api.marshal_with(response_success_message, code=204, description="成功彻底删除用户对象!")
    @login_require
    def delete(self, pk):
        """彻底删除用户对象"""
        return super(UserItem, self).delete(pk)

    def get_instance(self, pk, is_enable):
        instance = self.db.session.query(self.model).filter_by(is_enable=is_enable, id=pk).first()
        if instance is None:
            raise ProfileError(code=404, message={
                "pk": "No enable instance's pk is {0}!".format(pk)
            })
        return instance

    def perform_instance(self, pk, is_enable, body_data):
        instance = self.get_instance(pk, is_enable)
        instance.nickname = body_data["nickname"]
        return instance


@api.route('/<int:pk>/enable/')
@api.param('pk', '需要查找的用户ID')
@api.response(400, '参数形式有误', error_message)
class UserEnable(ResourceEnable):
    model = User
    db = db

    @api.marshal_with(response_user_item_success, code=200, description="成功激活用户对象!")
    @login_require
    def get(self, pk):
        """激活用户对象"""
        return super(UserEnable, self).get(pk)

    @api.marshal_with(response_success_message, code=204, description="成功禁用用户对象!")
    @login_require
    def delete(self, pk):
        """禁用用户对象(逻辑删除)"""
        return super(UserEnable, self).delete(pk)

    def get_instance(self, pk, is_enable):
        instance = self.db.session.query(self.model).filter_by(is_enable=is_enable, id=pk).first()
        if instance is None:
            raise ProfileError(code=404, message={
                "pk": "No enable instance's pk is {0}!".format(pk)
            })
        return instance

    def perform_enable(self, pk):
        instance = self.get_instance(pk, False)
        instance.disable_time = None
        instance.is_enable = True
        return instance

    def perform_disable(self, pk):
        instance = self.get_instance(pk, True)
        instance.disable_time = datetime.now()
        instance.is_enable = False
        return instance


@api.route('/<int:pk>/email/')
@api.param('pk', '需要查找的用户ID')
@api.response(400, '参数形式有误', error_message)
class ChangeEmail(ResourcePerform):
    model = User
    db = db

    @api.marshal_with(response_user_item_success, code=200, description="成功修改用户邮箱!")
    @api.expect(request_user_email)
    @login_require
    def put(self, pk):
        """修改用户邮箱"""
        return super(ChangeEmail, self).put(pk)

    def get_instance(self, pk, is_enable):
        instance = self.db.session.query(self.model).filter_by(is_enable=is_enable, id=pk).first()
        if instance is None:
            raise ProfileError(code=404, message={
                "pk": "No enable instance's pk is {0}!".format(pk)
            })
        return instance

    def perform_instance(self, pk, is_enable, body_data):
        instance = self.get_instance(pk, is_enable)
        if self.db.session.query(self.model).filter_by(email=body_data["email"]).first() is not None:
            raise ProfileError(code=404, message={
                "email": "The email named {0} is already exist!".format(body_data["email"])
            })
        instance.email = body_data["email"]
        return instance


@api.route('/<int:pk>/username/')
@api.param('user_id', '需要查找的用户ID')
@api.response(400, '参数形式有误', error_message)
class ChangeUsername(ResourcePerform):
    model = User
    db = db

    @api.marshal_with(response_user_item_success, code=200, description="成功修改用户名!")
    @api.expect(request_user_username)
    @login_require
    def put(self, pk):
        """修改用户名(仅一次)"""
        return super(ChangeUsername, self).put(pk)

    def get_instance(self, pk, is_enable):
        instance = self.db.session.query(self.model).filter_by(is_enable=is_enable, id=pk).first()
        if instance is None:
            raise ProfileError(code=404, message={
                "pk": "No enable instance's pk is {0}!".format(pk)
            })
        return instance

    def perform_instance(self, pk, is_enable, body_data):
        instance = self.get_instance(pk, is_enable)
        if instance.is_changed:
            raise ProfileError(code=404, message={
                "is_changed": "You can change your username only once!"
            })
        username_exist = db.session.query(User).filter_by(username=body_data["username"]).first()
        if username_exist is not None or "@" in body_data["username"]:
            raise ProfileError(code=404, message={
                "username": "The username named {0} is already exist or "
                            "like email(can not be email)!".format(body_data["username"])
            })
        instance.username = body_data["username"]
        instance.is_changed = True
        return instance


@api.route('/<int:pk>/password/')
@api.param('user_id', '需要查找的用户ID')
@api.response(400, '参数形式有误', error_message)
class ChangePassword(ResourcePerform):
    model = User
    db = db

    @api.marshal_with(response_user_item_success, code=200, description="成功修改用户密码!")
    @api.expect(request_user_password)
    @login_require
    def put(self, pk):
        """修改用户密码"""
        return super(ChangePassword, self).put(pk)

    def get_instance(self, pk, is_enable):
        instance = self.db.session.query(self.model).filter_by(is_enable=is_enable, id=pk).first()
        if instance is None:
            raise ProfileError(code=404, message={
                "pk": "No enable instance's pk is {0}!".format(pk)
            })
        return instance

    def perform_instance(self, pk, is_enable, body_data):
        instance = self.get_instance(pk, is_enable)
        if not instance.check_password(body_data["old_password"]):
            raise ProfileError(code=404, message={
                "old_password": "Old password wrong!".format(pk)
            })
        instance.set_password(body_data["new_password"])
        return instance


@api.route('/<int:pk>/password/reset/')
@api.param('user_id', '需要查找的用户ID')
@api.response(400, '参数形式有误', error_message)
class ResetPassword(ResourcePerform):
    model = User
    db = db

    @api.marshal_with(response_user_item_success, code=200, description="成功修改用户密码!")
    @api.expect(request_user_password)
    @login_require
    def put(self, pk):
        """重置用户密码"""
        return super(ResetPassword, self).put(pk)

    def get_instance(self, pk, is_enable):
        instance = self.db.session.query(self.model).filter_by(is_enable=is_enable, id=pk).first()
        if instance is None:
            raise ProfileError(code=404, message={
                "pk": "No enable instance's pk is {0}!".format(pk)
            })
        return instance

    def perform_instance(self, pk, is_enable, body_data):
        instance = self.get_instance(pk, is_enable)
        if not instance.check_password(body_data["old_password"]):
            raise ProfileError(code=404, message={
                "old_password": "Old password wrong!".format(pk)
            })
        instance.set_password(body_data["new_password"])
        return instance


@api.route('/<int:pk>/permission/')
@api.param('user_id', '需要查找的用户ID')
@api.response(400, '参数形式有误', error_message)
class ChangePermission(ResourcePerform):
    model = User
    db = db

    @api.marshal_with(response_user_item_success, code=200, description="成功修改用户权限!")
    @api.expect(request_user_permission)
    @login_require
    def put(self, pk):
        """修改用户权限(暂定)"""
        return super(ChangePermission, self).put(pk)

    def get_instance(self, pk, is_enable):
        instance = self.db.session.query(self.model).filter_by(is_enable=is_enable, id=pk).first()
        if instance is None:
            raise ProfileError(code=404, message={
                "pk": "No enable instance's pk is {0}!".format(pk)
            })
        return instance

    def perform_instance(self, pk, is_enable, body_data):
        instance = self.get_instance(pk, is_enable)
        instance.permission = body_data["permission"]
        return instance


@api.route('/username/')
@api.response(400, '参数形式有误', error_message)
class ValidateUsername(ResourceValidate):

    @api.marshal_with(response_success_message, code=200, description="用户名可用!")
    @api.expect(parser_username)
    @login_require
    def get(self):
        """判断用户名是否可用"""
        return super(ValidateUsername, self).get()

    def perform_validate(self, args):
        instance_exist = self.model.query.filter_by(username=args["username"]).first()
        if instance_exist is not None or "@" in args["username"]:
            raise ProfileError(code=404, message={
                "username": "The username named {0} is already exist or "
                            "like email(can not be email)!".format(args["username"])
            })
        return True


@api.route('/email/')
@api.response(400, '参数形式有误', error_message)
class ValidateEmail(ResourceValidate):

    @api.marshal_with(response_success_message, code=200, description="用户邮箱可用!")
    @api.expect(parser_email)
    @login_require
    def get(self):
        """判断邮箱是否可用"""
        return super(ValidateEmail, self).get()

    def perform_validate(self, args):
        instance_exist = self.model.query.filter_by(email=args["email"]).first()
        if instance_exist is not None:
            raise ProfileError(code=404, message={
                "email": "The email named {0} is already exist!".format(args["email"])
            })
        return True
