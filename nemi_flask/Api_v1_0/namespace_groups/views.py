from flask import g, request
from sqlalchemy import or_
from datetime import datetime

from models import User, db, Group, Space, Bucket, File

from ..utills.nemi_framework import ResourceList, ResourceCreate
from ..utills.nemi_framework import ResourceItem, ResourceEdit, ResourceDelete
from ..utills.nemi_framework import ResourceHit, ResourceValidate
from ..utills.response_init import ProfileError
from ..utills.wraps_define import login_require

from ..namespace_auth.api_init import error_message

from ..namespace_auth.api_init import parser, come_out_success
from .api_init import api, come_in_group_create, come_in_group_edit
from .api_init import come_out_group_list_success, come_out_group_item_success

from .group_action import group_disable, group_delete, group_enable


@api.route('/')
@api.response(400, '参数形式有误')
class GroupListCreate(ResourceList, ResourceCreate):
    list_parser = parser
    model = Group
    db = db

    @api.marshal_with(come_out_group_list_success, code=200, description="成功列出群组列表!")
    @api.expect(parser)
    @login_require
    def get(self):
        """列出群组列表"""
        return super(GroupListCreate, self).get()

    def get_instances(self, is_disable, order_object, page_index, page_size, args):
        instances = self.model.query.filter(self.model.is_enable != is_disable,
                                            self.model.creator_id == g.login_user.id).order_by(order_object) \
            .paginate(page=page_index, per_page=page_size, error_out=False)
        return instances

    @api.marshal_with(come_out_group_item_success, code=201, description="成功创建群组对象!")
    @api.expect(come_in_group_create)
    @login_require
    def post(self):
        """创建群组对象"""
        return super(GroupListCreate, self).post()

    def create_instance(self, body_data):
        """
        重载修改后:
        *.将password字段加密

        :param body_data: 创建对象时的传入数据
        :return: instance: 创建操作后的对象
        """
        body_data["creator_id"] = g.login_user.id
        # 判断该模型是否支持所有输入属性
        for item in body_data:
            if not hasattr(self.model, item):
                del body_data[item]
        # 创建对象
        group = self.model(**body_data)
        group.users = [g.login_user, ]
        db.session.add(group)
        db.session.commit()

        # 创建空间
        space_data = {
            "name": group.name + "'s private space",
            "space_type": "group",
            "own_group_id": group.id
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
            "creator_id": g.login_user.id,
            "bucket_id": bucket.id
        }
        folder_root = File(**bucket_data)
        db.session.add(folder_root)
        db.session.commit()

        # 关联空间与根目录
        space.root_folder = folder_root
        db.session.commit()

        return group


@api.route('/<int:pk>')
@api.param('pk', '需要查找的群组ID')
@api.response(400, '参数形式有误')
class GroupItemEditDisable(ResourceItem, ResourceEdit, ResourceDelete):
    model = Group
    db = db

    @api.marshal_with(come_out_group_item_success, code=200, description="成功获取群组对象!")
    @login_require
    def get(self, pk):
        """获取群组对象"""
        return super(GroupItemEditDisable, self).get(pk)

    @api.marshal_with(come_out_group_item_success, code=200, description="成功修改群组对象信息!")
    @api.expect(come_in_group_edit)
    @login_require
    def put(self, pk):
        """修改群组对象信息"""
        return super(GroupItemEditDisable, self).put(pk)

    @api.marshal_with(come_out_success, code=204, description="成功禁用群组对象!")
    @login_require
    def delete(self, pk):
        """禁用群组对象"""
        return super(GroupItemEditDisable, self).delete(pk)

    def delete_instance(self, instance):
        """
        重载修改后:
        *.逻辑删除
        *.若角色为管理员，禁用所有创建的用户

        :param instance: 需要做删除操作的对象
        :return: True: 删除操作完成
        """
        group_disable(instance, self.db)
        return True


@api.route('/<int:pk>/enable/')
@api.param('pk', '需要查找的用户ID')
@api.response(400, '参数形式有误')
class GroupHit(ResourceHit):
    model = Group
    db = db

    @api.marshal_with(come_out_group_item_success, code=200, description="成功激活用户对象!")
    @login_require
    def get(self, pk):
        """激活用户对象"""
        return super(GroupHit, self).get(pk)

    def get_instance(self, pk, is_disable=False):
        """
        重载修改后:
        *.获取禁用的用户

        :param pk: 对象的主键值
        :param is_disable: 是否禁用
        :return: instance: 查询到的对象
        """
        is_disable = True
        return super(GroupHit, self).get_instance(pk, is_disable)

    def hit_instance(self, instance):
        """
        重载修改后:
        *.若角色为管理员，激活所有创建的用户

        :param instance: 需要做撞击操作的对象
        :return: instance: 撞击完成的对象
        """
        group_enable(instance, self.db)
        return True


@api.route('/<int:pk>/destroy/')
@api.param('pk', '需要查找的用户ID')
@api.response(400, '参数形式有误')
class GroupDelete(ResourceDelete):
    model = Group
    db = db

    @api.marshal_with(come_out_success, code=204, description="成功彻底删除用户对象!")
    @login_require
    def delete(self, pk):
        """彻底删除用户对象"""
        return super(GroupDelete, self).delete(pk)

    def get_instance(self, pk, is_disable=False):
        """
        重载修改后:
        *.获取禁用的用户

        :param pk: 对象的主键值
        :param is_disable: 是否禁用
        :return: instance: 查询到的对象
        """
        is_disable = True
        return super(GroupDelete, self).get_instance(pk, is_disable)

    def delete_instance(self, instance):
        """
        重载修改后:
        *.若角色为管理员，删除所有由该管理员创建的用户

        :param instance: 需要做删除操作的对象
        :return: True: 删除操作完成
        """
        group_delete(instance, self.db)
        return True


@api.route('/members/<int:pk>')
@api.param('pk', '需要查找的群组ID')
@api.response(400, '参数形式有误')
class GroupMember(ResourceEdit):
    model = Group
    db = db

    @login_require
    def put(self, pk):
        """修改群组对象信息"""
        instance = self.get_instance(pk)
        users = []
        for item in request.json.get("users"):
            users.append(self.db.session.query(User).filter_by(id=item).first())
        instance.users = users
        self.db.session.commit()
        return True
