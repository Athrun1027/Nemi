from models import db, File
from flask import g

from ..utills.nemi_framework import ResourceList, ResourceCreate, ResourceEdit
from ..utills.nemi_framework import ResourceItem, ResourceEdit, ResourceDelete
from ..utills.nemi_framework import ResourceHit, ResourceValidate

from ..utills.response_init import ProfileError, success_response
from ..utills.wraps_define import login_require

from ..namespace_auth.api_init import come_out_success
from .api_init import api, parser
from .api_init import come_out_resource_list_success
from .api_init import come_out_resource_item_success
from .api_init import come_in_file_edit, come_in_file_move
from ..namespace_tags.views import flash_tags

from .resource_action import resource_disable, get_folder_size, resource_enable, resource_delete


@api.route('/')
@api.response(400, '参数形式有误')
class ResourceCreate(ResourceList):
    list_parser = parser
    model = File
    db = db

    @api.marshal_with(come_out_resource_list_success, code=200, description="成功列出资源列表!")
    @api.expect(parser)
    # @login_require
    def get(self):
        """列出资源列表"""
        return super(ResourceCreate, self).get()

    def get_instances(self, is_disable, order_object, page_index, page_size, args):
        """
        重载
        *.根据根目录判断

        :param is_disable: 是否禁用
        :param order_object: 排序的依据
        :param page_index: 分页的页码
        :param page_size: 分页的大小
        :param args: 其他内容
        :return: instances: 分页后的对象列表
        """
        folder_id = args.get("folder_id")
        instances = self.model.query.filter(self.model.is_enable != is_disable, self.model.folder_id == folder_id, )\
            .order_by(order_object).paginate(page=page_index, per_page=page_size, error_out=False)
        return instances


@api.route('/dead/')
@api.response(400, '参数形式有误')
class ResourceListDisable(ResourceList):
    list_parser = parser
    model = File
    db = db

    @api.marshal_with(come_out_resource_list_success, code=200, description="成功列出资源列表!")
    @api.expect(parser)
    @login_require
    def get(self):
        """列出禁用资源列表"""
        return super(ResourceListDisable, self).get()

    def get_instances(self, is_disable, order_object, page_index, page_size, args):
        """
        重载
        *.根据根目录判断

        :param is_disable: 是否禁用
        :param order_object: 排序的依据
        :param page_index: 分页的页码
        :param page_size: 分页的大小
        :param args: 其他内容
        :return: instances: 分页后的对象列表
        """
        instances = self.model.query.filter(self.model.is_enable != is_disable, self.model.creator_id == g.login_user.id)\
            .order_by(order_object).paginate(page=page_index, per_page=page_size, error_out=False)
        return instances


@api.route('/<int:pk>')
@api.param('pk', '需要查找的文件ID')
@api.response(400, '参数形式有误')
class ResourceItemEditDisable(ResourceItem, ResourceEdit, ResourceDelete):
    model = File
    db = db

    @api.marshal_with(come_out_resource_item_success, code=200, description="成功获取资源对象!")
    @login_require
    def get(self, pk):
        """获取资源对象"""
        instance = self.get_instance(pk)
        if instance.object_type == "folder":
            instance.object_size = get_folder_size(instance)
        return success_response(data=instance)

    @api.marshal_with(come_out_resource_item_success, code=200, description="成功修改资源对象信息!")
    @api.expect(come_in_file_edit)
    @login_require
    def put(self, pk):
        """修改资源对象信息"""
        return super(ResourceItemEditDisable, self).put(pk)

    @api.marshal_with(come_out_success, code=204, description="成功禁用资源对象!")
    @login_require
    def delete(self, pk):
        """禁用资源对象"""
        return super(ResourceItemEditDisable, self).delete(pk)

    def delete_instance(self, instance):
        """
        重载修改后:
        *.逻辑删除
        *.禁用所有内部的资源

        :param instance: 需要做删除操作的对象
        :return: True: 删除操作完成
        """
        resource_disable(instance, self.db)
        return True


@api.route('/<int:pk>/enable/')
@api.param('pk', '需要查找的资源ID')
@api.response(400, '参数形式有误')
class ResourceEnable(ResourceHit):
    model = File
    db = db

    @api.marshal_with(come_out_resource_item_success, code=200, description="成功激活资源对象!")
    @login_require
    def get(self, pk):
        """激活资源对象"""
        return super(ResourceEnable, self).get(pk)

    def get_instance(self, pk, is_disable=False):
        """
        重载修改后:
        *.获取禁用的用户

        :param pk: 对象的主键值
        :param is_disable: 是否禁用
        :return: instance: 查询到的对象
        """
        is_disable = True
        return super(ResourceEnable, self).get_instance(pk, is_disable)

    def hit_instance(self, instance):
        """
        重载修改后:
        *.激活所有内部的资源

        :param instance: 需要做撞击操作的对象
        :return: instance: 撞击完成的对象
        """
        resource_enable(instance, self.db)
        return True


@api.route('/<int:pk>/destroy/')
@api.param('pk', '需要查找的资源ID')
@api.response(400, '参数形式有误')
class ResourceDestroy(ResourceDelete):
    model = File
    db = db

    @api.marshal_with(come_out_success, code=204, description="成功彻底删除资源对象!")
    @login_require
    def delete(self, pk):
        """彻底删除资源对象"""
        return super(ResourceDestroy, self).delete(pk)

    def get_instance(self, pk, is_disable=False):
        """
        重载修改后:
        *.获取禁用的资源

        :param pk: 对象的主键值
        :param is_disable: 是否禁用
        :return: instance: 查询到的对象
        """
        is_disable = True
        return super(ResourceDestroy, self).get_instance(pk, is_disable)

    def delete_instance(self, instance):
        """
        重载修改后:
        *.删除所有内部的资源

        :param instance: 需要做删除操作的对象
        :return: True: 删除操作完成
        """
        resource_delete(instance, self.db)
        flash_tags()
        return True


@api.route('/<int:pk>/move/')
@api.param('pk', '需要查找的资源ID')
@api.response(400, '参数形式有误')
class ResourceMove(ResourceEdit):
    model = File
    db = db

    @api.marshal_with(come_out_resource_item_success, code=204, description="成功移动资源对象!")
    @api.expect(come_in_file_move)
    @login_require
    def put(self, pk):
        """移动资源对象"""
        return super(ResourceMove, self).put(pk)


@api.route('/<int:pk>/copy/')
@api.param('pk', '需要查找的资源ID')
@api.response(400, '参数形式有误')
class ResourceCopy(ResourceEdit):
    model = File
    db = db

    @api.marshal_with(come_out_resource_item_success, code=204, description="成功复制资源对象!")
    @api.expect(come_in_file_move)
    @login_require
    def put(self, pk):
        """复制资源对象"""
        return super(ResourceCopy, self).put(pk)

    def edit_instance(self, instance, body_data):
        instance_new = dict()
        instance_new["object_name"] = instance.object_name
        instance_new["object_type"] = instance.object_type
        instance_new["object_size"] = instance.object_size
        instance_new["object_uuid"] = instance.object_uuid
        instance_new["creator_id"] = instance.creator_id
        instance_new["folder_id"] = body_data.get("folder_id")
        instance_new["bucket_id"] = instance.bucket_id
        instance_new["tags"] = instance.tags
        instance_new_object = self.model(**instance_new)
        self.db.session.add(instance_new_object)
        self.db.session.commit()
        return instance_new_object


@api.route('/root/<int:pk>')
@api.param('pk', '需要查找的文件ID')
@api.response(400, '参数形式有误')
class ResourceRootFolder(ResourceItem):
    model = File
    db = db

    def get(self, pk):
        """获取资源对象"""
        instance = self.get_instance(pk)
        root = list()
        root.append({
            "id": instance.id,
            "object_name": instance.object_name
        })
        while instance.folder_id is not None:
            instance = self.get_instance(instance.folder_id)
            root.append({
                "id": instance.id,
                "object_name": instance.object_name
            })
        return success_response(data=root)
