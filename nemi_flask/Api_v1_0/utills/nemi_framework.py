from flask import request, g
from sqlalchemy import and_
from flask_restplus import Resource
from sqlalchemy.exc import IntegrityError


from .response_init import success_response, ProfileError

__all__ = [
    "ResourceBase", "ResourceList", "ResourceCreate", "ResourceItem",
    "ResourceEdit", "ResourceDelete", "ResourceHit", "ResourceValidate"
]


class ResourceBase(object):
    model = None
    db = None

    def get_instances(self, is_disable, order_object, page_index, page_size, args):
        """
        分页获取对象列表

        :param is_disable: 是否禁用
        :param order_object: 排序的依据
        :param page_index: 分页的页码
        :param page_size: 分页的大小
        :param args: 其他内容
        :return: instances: 分页后的对象列表
        """
        instances = self.model.query.filter(self.model.is_enable != is_disable).order_by(order_object) \
            .paginate(page=page_index, per_page=page_size, error_out=False)
        return instances

    def get_instance(self, pk, is_disable=False):
        """
        单独获取对象，默认为未禁用对象
        若访问禁用对象:
        is_disable = True
        后super该逻辑

        :param pk: 对象的主键值
        :param is_disable: 是否禁用
        :return: instance: 查询到的对象
        """
        instance = self.db.session.query(self.model).filter(and_(
            self.model.is_enable != is_disable, self.model.id == pk)).first()
        if instance is None:
            raise ProfileError(code=404, message={
                "pk": "No match instance's pk is {0}!".format(pk)
            })
        return instance


class ResourceList(Resource, ResourceBase):
    list_parser = None

    def get(self):
        """列出资源列表"""
        args = self.list_parser.parse_args()
        # 赋默认值
        page_index = args.get("PageIndex") or 1
        page_size = args.get("PageSize") or 10
        order_by = args.get("OrderBy") or "id"
        is_disable = bool(args.get("Disable"))
        # 判断该模型是否支持此次排序需求
        if not hasattr(self.model, order_by) and not hasattr(self.model, order_by[1:]):
            raise ProfileError(code=400, message={
                "order_by": "Not support this field!"
            })
        # 判断排序的正负
        if order_by.startswith("-"):
            order_by = order_by[1:]
            order_object = getattr(self.model, order_by).desc()
        else:
            order_object = getattr(self.model, order_by)
        # 得到符合条件的对象列表
        instances = self.get_instances(is_disable, order_object, page_index, page_size, args)
        # 判断分页的参数是否超过范围
        if instances.page > instances.pages and instances.pages:
            raise ProfileError(code=400, message={
                "PageIndex": "Out of the max range!"
            })
        return success_response(data=instances.items)


class ResourceCreate(Resource, ResourceBase):

    def post(self):
        """创建资源对象"""
        body_data = request.get_json()
        try:
            # 创建对象
            instance = self.create_instance(body_data)
        except IntegrityError as e:
            detail = getattr(getattr(e, "orig"), "args")
            raise ProfileError(code=400, message={
                "SQL": detail[1]
            })
        return success_response(data=instance), 201

    def create_instance(self, body_data):
        """
        若其他需要改变的数据，请重载修改后super该逻辑

        :param body_data: 创建对象时的传入数据
        :return: instance: 创建操作后的对象
        """
        body_data["creator_id"] = g.login_user.id
        # 判断该模型是否支持所有输入属性
        for item in body_data:
            if not hasattr(self.model, item):
                raise ProfileError(code=400, message={
                    str(item): str(body_data[item]) + " not support!"
                })
        # 创建对象
        instance = self.model(**body_data)
        self.db.session.add(instance)
        self.db.session.commit()
        return instance


class ResourceItem(Resource, ResourceBase):

    def get(self, pk):
        """获取资源对象"""
        instance = self.get_instance(pk)
        return success_response(data=instance)


class ResourceEdit(Resource, ResourceBase):

    def put(self, pk):
        """修改资源对象信息"""
        body_data = request.get_json()
        # 获取对象
        instance = self.get_instance(pk)
        try:
            # 修改对象属性
            instance = self.edit_instance(instance, body_data)
        except IntegrityError as e:
            detail = getattr(getattr(e, "orig"), "args")
            raise ProfileError(code=400, message={
                "SQL": detail[1]
            })
        return success_response(data=instance)

    def edit_instance(self, instance, body_data):
        """
        若其他需要改变的数据，请重载修改后super该逻辑

        :param instance: 需要修改属性的对象
        :param body_data: 修改对象属性时的传入数据
        :return: instance: 修改属性完成的对象
        """
        for item in body_data:
            # 判断该模型是否支持所有输入属性
            if hasattr(self.model, item):
                # 设置属性
                setattr(instance, item, body_data[item])
        self.db.session.commit()
        return instance


class ResourceDelete(Resource, ResourceBase):

    def delete(self, pk):
        """删除资源对象"""
        instance = self.get_instance(pk)
        self.delete_instance(instance)
        return success_response(code=204)

    def delete_instance(self, instance):
        """
        若逻辑不为物理删除，请重载整个逻辑

        :param instance: 需要做删除操作的对象
        :return: True: 删除操作完成
        """
        self.db.session.delete(instance)
        self.db.session.commit()
        return True


class ResourceHit(Resource, ResourceBase):

    def get(self, pk):
        """撞击资源对象"""
        instance = self.get_instance(pk)
        self.hit_instance(instance)
        return success_response(data=instance)

    def hit_instance(self, instance):
        """
        若撞击逻辑复杂，请重载整个撞击逻辑

        :param instance: 需要做撞击操作的对象
        :return: instance: 撞击完成的对象
        """
        if hasattr(self.model, "disable_time") and hasattr(self.model, "is_enable"):
            instance.disable_time = None
            instance.is_enable = True
        self.db.session.commit()
        return True


class ResourceValidate(Resource, ResourceBase):
    validate_parser = None

    def get(self):
        """判断资源字段是否可用"""
        args = self.validate_parser.parse_args()
        self.perform_validate(args)
        return success_response(data="This field is available!")

    def perform_validate(self, args):
        """
        判断逻辑请重载整个判断逻辑

        :param args: 需要判断的所有字段
        :return: True: 判断操作完成
        """
        if hasattr(args, "email") and self.validate_parser:
            if "@" not in args["email"]:
                raise ProfileError(code=404, message={
                    "email": "the email is not validate!"
                })
        return True
