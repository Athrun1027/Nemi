from models import db, Space

from ..utills.nemi_framework import ResourceItem

from ..utills.wraps_define import login_require
from ..utills.response_init import ProfileError


from .api_init import api, come_out_space_success


@api.route('/<int:pk>')
@api.param('pk', '需要查找的空间ID')
@api.response(400, '参数形式有误')
class SpaceItem(ResourceItem):
    model = Space
    db = db

    @api.marshal_with(come_out_space_success, code=200, description="成功获取空间对象!")
    @login_require
    def get(self, pk):
        """获取空间对象"""
        return super(SpaceItem, self).get(pk)

    def get_instance(self, pk, is_disable=False):
        """
        重载后
        * 删除is_disable的判断

        :param pk: 对象的主键值
        :param is_disable: 是否禁用
        :return: instance: 查询到的对象
        """
        instance = self.db.session.query(self.model).filter_by(id=pk).first()
        if instance is None:
            raise ProfileError(code=404, message={
                "pk": "No match instance's pk is {0}!".format(pk)
            })
        return instance
