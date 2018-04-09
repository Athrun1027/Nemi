from models import db, Bucket, File

from ..utills.nemi_framework import ResourceItem, ResourceCreate

from ..utills.wraps_define import login_require
from ..utills.response_init import ProfileError


from .api_init import api, come_out_bucket_success, come_in_bucket_add


@api.route('/<int:pk>')
@api.param('pk', '需要查找的桶ID')
@api.response(400, '参数形式有误')
class BucketItem(ResourceItem):
    model = Bucket
    db = db

    @api.marshal_with(come_out_bucket_success, code=200, description="成功获取桶对象!")
    @login_require
    def get(self, pk):
        """获取桶对象"""
        return super(BucketItem, self).get(pk)

    def get_instance(self, pk, is_disable=False):
        """
        重载后
        * 删除is_disable的判断
        * 加入数量和小大的计算

        :param pk: 对象的主键值
        :param is_disable: 是否禁用
        :return: instance: 查询到的对象
        """
        instance = self.db.session.query(self.model).filter_by(id=pk).first()
        if instance is None:
            raise ProfileError(code=404, message={
                "pk": "No match instance's pk is {0}!".format(pk)
            })
        files = db.session.query(File).filter(File.bucket_id == instance.id, File.object_type != "folder").all()
        size_count = 0
        num_count = 0
        for item in files:
            size_count += int(item.object_size)
            num_count += 1
        instance.size_count = size_count
        instance.num_count = num_count
        return instance


@api.route('/')
@api.response(400, '参数形式有误')
class BucketAdd(ResourceCreate):
    model = Bucket
    db = db

    @api.marshal_with(come_out_bucket_success, code=201, description="成功增加桶对象!")
    @api.expect(come_in_bucket_add)
    @login_require
    def post(self):
        """增加桶对象"""
        return super(BucketAdd, self).post()

    def create_instance(self, body_data):
        """
        重载修改后:
        *.去除创建人

        :param body_data: 创建对象时的传入数据
        :return: instance: 创建操作后的对象
        """
        # 判断该模型是否支持所有输入属性
        for item in body_data:
            if not hasattr(self.model, item):
                del body_data[item]
        # 创建对象
        bucket = self.model(**body_data)
        db.session.add(bucket)
        db.session.commit()
        bucket.size_count = 0
        bucket.num_count = 0
        return bucket
