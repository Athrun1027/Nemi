from werkzeug.security import generate_password_hash
from flask import g

from models import User, db, Space, Bucket, File

from ..utills.nemi_framework import ResourceList, ResourceCreate
from ..utills.nemi_framework import ResourceItem, ResourceEdit, ResourceDelete
from ..utills.nemi_framework import ResourceHit, ResourceValidate

from ..utills.response_init import ProfileError
from ..utills.wraps_define import login_require


from ..namespace_auth.api_init import parser, come_out_success
from .api_init import api
from .api_init import come_out_user_list_success, come_out_user_item_success
from .api_init import come_in_user_create, come_in_user_edit
from .api_init import come_in_user_email, come_in_user_username
from .api_init import come_in_user_password, come_in_user_permission
from .api_init import come_in_reset_password
from .api_init import parser_email, parser_username

from .user_action import user_disable, user_delete, user_enable


@api.route('/')
@api.response(400, '参数形式有误')
class UserListCreate(ResourceList, ResourceCreate):
    list_parser = parser
    model = User
    db = db

    @api.marshal_with(come_out_user_list_success, code=200, description="成功列出用户列表!")
    @api.expect(parser)
    def get(self):
        """列出用户列表"""
        return super(UserListCreate, self).get()

    @api.marshal_with(come_out_user_item_success, code=201, description="成功创建用户对象!")
    @api.expect(come_in_user_create)
    @login_require
    def post(self):
        """创建用户对象"""
        return super(UserListCreate, self).post()

    def create_instance(self, body_data):
        """
        重载修改后:
        *.将password字段加密

        :param body_data: 创建对象时的传入数据
        :return: instance: 创建操作后的对象
        """
        password = generate_password_hash(body_data["password"], method="pbkdf2:sha256")
        body_data["password"] = password
        body_data["creator_id"] = g.login_user.id
        # 判断该模型是否支持所有输入属性
        for item in body_data:
            if not hasattr(self.model, item):
                del body_data[item]
        # 创建对象
        user = self.model(**body_data)
        db.session.add(user)
        db.session.commit()

        # 创建空间
        space_data = {
            "name": user.username + "'s private space",
            "space_type": "private",
            "own_user_id": user.id
        }
        space = Space(**space_data)
        db.session.add(space)
        db.session.commit()

        # 创建桶
        bucket_data = {
            "name": space.name + "'s 1st bucket",
            "space_id": space.id
        }
        bucket = Bucket(**bucket_data)
        db.session.add(bucket)
        db.session.commit()

        # 创建空间根目录
        bucket_data = {
            "object_name": space.name + "'s root",
            "object_type": "folder",
            "object_size": 0,
            "creator_id": user.id,
            "bucket_id": bucket.id
        }
        folder_root = File(**bucket_data)
        db.session.add(folder_root)
        db.session.commit()

        # 关联空间与根目录
        space.root_folder = folder_root
        db.session.commit()

        return user


@api.route('/<int:pk>')
@api.param('pk', '需要查找的用户ID')
@api.response(400, '参数形式有误')
class UserItemEditDisable(ResourceItem, ResourceEdit, ResourceDelete):
    model = User
    db = db

    @api.marshal_with(come_out_user_item_success, code=200, description="成功获取用户对象!")
    @login_require
    def get(self, pk):
        """获取用户对象"""
        return super(UserItemEditDisable, self).get(pk)

    @api.marshal_with(come_out_user_item_success, code=200, description="成功修改用户对象信息!")
    @api.expect(come_in_user_edit)
    @login_require
    def put(self, pk):
        """修改用户对象信息"""
        return super(UserItemEditDisable, self).put(pk)

    @api.marshal_with(come_out_success, code=204, description="成功禁用用户对象!")
    @login_require
    def delete(self, pk):
        """禁用用户对象"""
        return super(UserItemEditDisable, self).delete(pk)

    def delete_instance(self, instance):
        """
        重载修改后:
        *.逻辑删除
        *.若角色为管理员，禁用所有创建的用户

        :param instance: 需要做删除操作的对象
        :return: True: 删除操作完成
        """
        user_disable(instance, self.db)
        return True


@api.route('/<int:pk>/enable/')
@api.param('pk', '需要查找的用户ID')
@api.response(400, '参数形式有误')
class UserHit(ResourceHit):
    model = User
    db = db

    @api.marshal_with(come_out_user_item_success, code=200, description="成功激活用户对象!")
    @login_require
    def get(self, pk):
        """激活用户对象"""
        return super(UserHit, self).get(pk)

    def get_instance(self, pk, is_disable=False):
        """
        重载修改后:
        *.获取禁用的用户

        :param pk: 对象的主键值
        :param is_disable: 是否禁用
        :return: instance: 查询到的对象
        """
        is_disable = True
        return super(UserHit, self).get_instance(pk, is_disable)

    def hit_instance(self, instance):
        """
        重载修改后:
        *.若角色为管理员，激活所有创建的用户

        :param instance: 需要做撞击操作的对象
        :return: instance: 撞击完成的对象
        """
        user_enable(instance, self.db)
        return True


@api.route('/<int:pk>/destroy/')
@api.param('pk', '需要查找的用户ID')
@api.response(400, '参数形式有误')
class UserDelete(ResourceDelete):
    model = User
    db = db

    @api.marshal_with(come_out_success, code=204, description="成功彻底删除用户对象!")
    @login_require
    def delete(self, pk):
        """彻底删除用户对象"""
        return super(UserDelete, self).delete(pk)

    def get_instance(self, pk, is_disable=False):
        """
        重载修改后:
        *.获取禁用的用户

        :param pk: 对象的主键值
        :param is_disable: 是否禁用
        :return: instance: 查询到的对象
        """
        is_disable = True
        return super(UserDelete, self).get_instance(pk, is_disable)

    def delete_instance(self, instance):
        """
        重载修改后:
        *.若角色为管理员，删除所有由该管理员创建的用户

        :param instance: 需要做删除操作的对象
        :return: True: 删除操作完成
        """
        user_delete(instance, self.db)
        return True


@api.route('/<int:pk>/email/')
@api.param('pk', '需要查找的用户ID')
@api.response(400, '参数形式有误')
class ChangeEmail(ResourceEdit):
    model = User
    db = db

    @api.marshal_with(come_out_user_item_success, code=200, description="成功修改用户邮箱!")
    @api.expect(come_in_user_email)
    @login_require
    def put(self, pk):
        """修改用户邮箱"""
        return super(ChangeEmail, self).put(pk)


@api.route('/<int:pk>/username/')
@api.param('pk', '需要查找的用户ID')
@api.response(400, '参数形式有误')
class ChangeUsername(ResourceEdit):
    model = User
    db = db

    @api.marshal_with(come_out_user_item_success, code=200, description="成功修改用户名!")
    @api.expect(come_in_user_username)
    @login_require
    def put(self, pk):
        """修改用户名(仅一次)"""
        return super(ChangeUsername, self).put(pk)

    def edit_instance(self, instance, body_data):
        """
        重载修改后:
        *.先判断是否已经修改过用户名

        :param instance: 需要修改属性的对象
        :param body_data: 修改对象属性时的传入数据
        :return: instance: 修改属性完成的对象
        """
        if instance.is_changed:
            raise ProfileError(code=404, message={
                "is_changed": "You can change your username only once!"
            })
        instance.is_changed = True
        return super(ChangeUsername, self).edit_instance(instance, body_data)


@api.route('/<int:pk>/password/')
@api.param('pk', '需要查找的用户ID')
@api.response(400, '参数形式有误')
class ChangePassword(ResourceEdit):
    model = User
    db = db

    @api.marshal_with(come_out_user_item_success, code=200, description="成功修改用户密码!")
    @api.expect(come_in_user_password)
    @login_require
    def put(self, pk):
        """修改用户密码"""
        return super(ChangePassword, self).put(pk)

    def edit_instance(self, instance, body_data):
        """
        重载修改后:
        *.判断旧密码是否匹配
        *.修改密码

        :param instance: 需要修改属性的对象
        :param body_data: 修改对象属性时的传入数据
        :return: instance: 修改属性完成的对象
        """
        if not instance.check_password(body_data["old_password"]):
            raise ProfileError(code=404, message={
                "old_password": "Old password wrong!"
            })
        instance.change_password(body_data["new_password"])
        self.db.session.commit()
        return instance


@api.route('/<int:pk>/password/reset/')
@api.param('pk', '需要查找的用户ID')
@api.response(400, '参数形式有误')
class ResetPassword(ResourceEdit):
    model = User
    db = db

    @api.marshal_with(come_out_user_item_success, code=200, description="成功修改用户密码!")
    @api.expect(come_in_reset_password)
    @login_require
    def put(self, pk):
        """重置用户密码"""
        return super(ResetPassword, self).put(pk)

    def edit_instance(self, instance, body_data):
        """
        重载修改后:
        *.修改密码

        :param instance: 需要修改属性的对象
        :param body_data: 修改对象属性时的传入数据
        :return: instance: 修改属性完成的对象
        """
        instance.change_password(body_data["password"])
        self.db.session.commit()
        return instance


@api.route('/<int:pk>/permission/')
@api.param('pk', '需要查找的用户ID')
@api.response(400, '参数形式有误')
class ChangePermission(ResourceEdit):
    model = User
    db = db

    @api.marshal_with(come_out_user_item_success, code=200, description="成功修改用户权限!")
    @api.expect(come_in_user_permission)
    @login_require
    def put(self, pk):
        """修改用户权限(暂定)"""
        return super(ChangePermission, self).put(pk)


@api.route('/username/')
@api.response(400, '参数形式有误')
class ValidateUsername(ResourceValidate):
    validate_parser = parser_username
    model = User
    db = db

    @api.marshal_with(come_out_success, code=200, description="用户名可用!")
    @api.expect(parser_username)
    @login_require
    def get(self):
        """判断用户名是否可用"""
        return super(ValidateUsername, self).get()

    def perform_validate(self, args):
        """
        重载修改后:
        *.判断该用户名是否存在
        *.判断是否为邮箱格式

        :param args: 需要判断的所有字段
        :return: True: 判断操作完成
        """
        instance_exist = self.model.query.filter_by(username=args["username"]).first()
        if instance_exist or "@" in args["username"]:
            raise ProfileError(code=404, message={
                "username": "The username named {0} is already exist or "
                            "like email(can not be email)!".format(args["username"])
            })
        return True


@api.route('/email/')
@api.response(400, '参数形式有误')
class ValidateEmail(ResourceValidate):
    validate_parser = parser_email
    model = User
    db = db

    @api.marshal_with(come_out_success, code=200, description="用户邮箱可用!")
    @api.expect(parser_email)
    @login_require
    def get(self):
        """判断邮箱是否可用"""
        return super(ValidateEmail, self).get()

    def perform_validate(self, args):
        """
        重载修改后:
        *.判断该邮件是否存在

        :param args: 需要判断的所有字段
        :return: True: 判断操作完成
        """
        instance_exist = self.model.query.filter_by(email=args["email"]).first()
        if instance_exist:
            raise ProfileError(code=404, message={
                "email": "The email named {0} is already exist!".format(args["email"])
            })
        return True
