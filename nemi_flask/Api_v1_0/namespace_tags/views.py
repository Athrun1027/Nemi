from models import db, File, Tag
from sqlalchemy import not_

from ..utills.nemi_framework import ResourceList, ResourceCreate
from ..utills.nemi_framework import ResourceItem, ResourceDelete

from ..utills.response_init import ProfileError, success_response
from ..utills.wraps_define import login_require


from ..namespace_auth.api_init import parser, come_out_success
from .api_init import api, come_in_tag_create, parser_tag
from .api_init import come_out_tag_list_success, come_out_tag_item_success


@api.route('/')
@api.response(400, '参数形式有误')
class TagListCreate(ResourceList, ResourceCreate):
    list_parser = parser_tag
    model = Tag
    db = db

    @api.marshal_with(come_out_tag_list_success, code=200, description="成功列出标签列表!")
    @api.expect(parser_tag)
    def get(self):
        """列出标签列表"""
        return super(TagListCreate, self).get()

    @api.marshal_with(come_out_tag_item_success, code=201, description="成功创建标签对象!")
    @api.expect(come_in_tag_create)
    @login_require
    def post(self):
        """创建标签对象"""
        return super(TagListCreate, self).post()

    def create_instance(self, body_data):
        tag = db.session.query(Tag).filter_by(name=body_data.get("name")).first()
        if tag is None:
            tag = Tag(name=body_data.get("name"))
            db.session.add(tag)
            db.session.commit()
        file = db.session.query(File).filter_by(id=body_data.get("file_id")).first()
        tag.files.append(file)
        db.session.commit()
        return tag

    def get_instances(self, is_disable, order_object, page_index, page_size, args):
        instances = self.model.query.all().order_by(order_object) \
            .paginate(page=page_index, per_page=page_size, error_out=False)
        return instances


@api.route('/<int:pk>')
@api.param('pk', '需要查找的标签ID')
@api.response(400, '参数形式有误')
class TagItemEdit(ResourceItem):
    model = Tag
    db = db

    @api.marshal_with(come_out_tag_item_success, code=200, description="成功获取标签对象!")
    @login_require
    def get(self, pk):
        """获取标签对象"""
        return super(TagItemEdit, self).get(pk)

    def get_instance(self, pk, is_disable=False):
        instance = self.db.session.query(self.model).filter_by(id=pk).first()
        if instance is None:
            raise ProfileError(code=404, message={
                "pk": "No match instance's pk is {0}!".format(pk)
            })
        return instance


@api.route('/<int:pk>/file/<int:file_id>/')
@api.param('pk', '需要查找的标签ID')
@api.response(400, '参数形式有误')
class TagItemDisable(ResourceDelete):
    model = Tag
    db = db

    @api.marshal_with(come_out_success, code=204, description="成功禁用标签对象!")
    @login_require
    def delete(self, pk, file_id):
        """禁用标签对象"""
        instance = self.get_instance(pk)
        file = db.session.query(File).filter_by(id=file_id).first()
        instance.files.remove(file)
        self.db.session.commit()
        if not len(instance.files):
            self.db.session.delete(instance)
            self.db.session.commit()
        return success_response(code=204)

    def get_instance(self, pk, is_disable=False):
        instance = self.db.session.query(self.model).filter_by(id=pk).first()
        if instance is None:
            raise ProfileError(code=404, message={
                "pk": "No match instance's pk is {0}!".format(pk)
            })
        return instance


def flash_tags():
    instances = db.session.query(Tag).filter(not_(Tag.files.any()))
    for item in instances:
        db.session.delete(item)
    db.session.commit()
    return True
