from flask import request
from flask_restplus import Resource

from .response_init import success_response, ProfileError


class ResourceList(Resource):
    list_parser = None
    model = None
    db = None

    def get(self):
        """列出资源列表"""
        args = self.list_parser.parse_args()
        page_index = args["PageIndex"] or 1
        page_size = args["PageSize"] or 10
        order_by = args["OrderBy"] or "id"
        is_disable = bool(args["Disable"])
        if not hasattr(self.model, order_by):
            raise ProfileError(code=400, message={
                "order_by": "Not support this field!"
            })
        if order_by.startswith("-"):
            order_by = order_by[1:]
            order_object = getattr(self.model, order_by).desc()
        else:
            order_object = getattr(self.model, order_by)
        instances = self.get_instances(is_disable, order_object, page_index, page_size)
        if instances.page > instances.pages and 0 != instances.pages:
            raise ProfileError(code=400, message={
                "PageIndex": "Out of the max range!"
            })
        return success_response(data=instances.items)

    def post(self):
        """创建资源对象"""
        body_data = request.get_json()
        instance = self.create_instance(body_data)
        self.db.session.add(instance)
        self.db.session.commit()
        return success_response(data=instance), 201

    def get_instances(self, is_disable, order_object, page_index, page_size):
        """
        eg:
        instances = self.model.query.filter(self.model.is_enable != is_disable).order_by(order_object) \
            .paginate(page=page_index, per_page=page_size, error_out=False)
        return instances

        :param is_disable:
        :param order_object:
        :param page_index:
        :param page_size:
        :return: instance
        """
        pass

    def create_instance(self, body_data):
        """
        eg:
        instance_exist = self.db.session.query(self.model).filter(...).first()
        if instance_exist is not None:
            raise ProfileError(code=400, message={...})
        instance = self.model(...)
        return instance

        :param body_data:
        :return: instance
        """
        pass


class ResourceItem(Resource):
    model = None
    db = None

    def get(self, pk):
        """获取资源对象"""
        instance = self.get_instance(pk, True)
        return success_response(data=instance)

    def put(self, pk):
        """修改资源对象信息"""
        body_data = request.get_json()
        instance = self.perform_instance(pk, True, body_data)
        self.db.session.commit()
        return success_response(data=instance)

    def delete(self, pk):
        """彻底删除资源对象"""
        instance = self.get_instance(pk, False)
        self.db.session.delete(instance)
        self.db.session.commit()
        return success_response(code=204)

    def get_instance(self, pk, is_enable):
        """
        eg:
        instance = self.db.session.query(self.model).filter_by(is_enable=is_enable, id=pk).first()
        if instance is None:
            raise ProfileError(code=404, message={...})
        return instance

        :param pk:
        :param is_enable:
        :return:
        """
        pass

    def perform_instance(self, pk, is_enable, body_data):
        """
        eg:
        instance = self.get_instance(pk, is_enable)
        instance.nickname = body_data["nickname"]
        ...
        return instance

        :param pk:
        :param is_enable:
        :param body_data:
        :return: instance
        """
        pass


class ResourceEnable(Resource):
    model = None
    db = None

    def get(self, pk):
        """激活资源对象"""
        instance = self.perform_enable(pk)
        self.db.session.commit()
        return success_response(data=instance)

    def delete(self, pk):
        """禁用资源对象(逻辑删除)"""
        self.perform_disable(pk)
        self.db.session.commit()
        return success_response(code=204)

    def get_instance(self, pk, is_enable):
        """
        eg:
        instance = self.db.session.query(self.model).filter_by(is_enable=is_enable, id=pk).first()
        if instance is None:
            raise ProfileError(code=404, message={...})
        return instance

        :param pk:
        :param is_enable:
        :return: instance
        """
        pass

    def perform_enable(self, pk):
        """
        eg:
        instance = self.get_instance(pk, False)
        instance.disable_time = None
        instance.is_enable = True
        ...
        return instance

        :param pk:
        :return: instance
        """
        pass

    def perform_disable(self, pk):
        """
        eg:
        instance = self.get_instance(pk, True)
        instance.disable_time = datetime.now()
        instance.is_enable = False
        ...
        return instance

        :param pk:
        :return: instance
        """
        pass


class ResourcePerform(Resource):
    model = None
    db = None

    def put(self, pk):
        """修改资源对象信息"""
        body_data = request.get_json()
        instance = self.perform_instance(pk, True, body_data)
        self.db.session.commit()
        return success_response(data=instance)

    def get_instance(self, pk, is_enable):
        """
        eg:
        instance = self.db.session.query(self.model).filter_by(is_enable=is_enable, id=pk).first()
        if instance is None:
            raise ProfileError(code=404, message={...})
        return instance

        :param pk:
        :param is_enable:
        :return: instance
        """
        pass

    def perform_instance(self, pk, is_enable, body_data):
        """
        eg:
        instance = self.get_instance(pk, is_enable)
        instance.nickname = body_data["nickname"]
        ...
        return instance

        :param pk:
        :param is_enable:
        :param body_data:
        :return: instance
        """
        pass


class ResourceValidate(Resource):
    validate_parser = None
    model = None
    db = None

    def get(self):
        """判断资源字段是否可用"""
        args = self.validate_parser.parse_args()
        self.perform_validate(args)
        return success_response(data="This field is available!")

    def perform_validate(self, args):
        """
        eg:
        instance_exist = self.model.query.filter_by(username=args[...]).first()
        if instance_exist is not None or "..." in args[...]:
            raise ProfileError(code=404, message={...})
        return True

        :param args:
        :return: True
        """
        pass
