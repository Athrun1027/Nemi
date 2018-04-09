from models import db, File

from ..utills.nemi_framework import ResourceCreate, ResourceItem
from ..utills.wraps_define import login_require
from ..utills.response_init import success_response


from .api_init import api, come_in_folder_create, come_out_folder_success


@api.route('/')
@api.response(400, '参数形式有误')
class FolderCreate(ResourceCreate):
    model = File
    db = db

    @api.marshal_with(come_out_folder_success, code=201, description="成功创建目录对象!")
    @api.expect(come_in_folder_create)
    @login_require
    def post(self):
        """创建目录对象"""
        return super(FolderCreate, self).post()


@api.route('/<int:pk>/tree/')
@api.param('pk', '需要查找的根目录ID')
@api.response(400, '参数形式有误')
class FolderTree(ResourceItem):
    model = File
    db = db

    @login_require
    def get(self, pk):
        """获取根目录树结构"""
        instance = self.get_instance(pk)
        tree_data = get_tree(instance)
        tree_data_all = {
            "key": pk,
            "title": "root folder",
            "children": tree_data
        }
        return success_response(data=tree_data_all)


def get_tree(instance):
    tree_data = []
    for item in instance.kids:
        item_structure = {
            "key": item.id,
            "title": item.object_name
        }
        if item.object_type == "folder":
            item_structure["children"] = get_tree(item)
        tree_data.append(item_structure)
    return tree_data
