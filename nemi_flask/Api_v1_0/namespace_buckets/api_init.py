from flask_restplus import fields, reqparse

from ..utills.response_init import ProfileError
from ..utills.flask_plus_profile import NamespaceProfile as Namespace, ArgumentProfile


api = Namespace('buckets', description='桶模块')

bucket_simple = api.model('bucket_simple', {
    'id': fields.Integer(description="桶ID"),
    'name': fields.String(description="桶名")
})

bucket = api.model('bucket', {
    'id': fields.Integer(description="桶ID"),
    'name': fields.String(description="桶名"),
    'size_count': fields.Integer(description="总大小"),
    'num_count': fields.Integer(description="总个数")
})

come_out_bucket_success = api.model('come_out_bucket_success', {
    'code': fields.Integer(description="状态码"),
    'success': fields.Boolean(description="是否成功"),
    'data': fields.Nested(model=bucket, description="内容数据")
})

come_in_bucket_add = api.model('come_in_bucket_add', {
    'space_id': fields.Integer(required=True, description="空间ID"),
    'name': fields.String(required=True, description="桶名称", min_length=6, max_length=60)
})


@api.errorhandler(ProfileError)
def profile_error(error):
    return {'code': error.code, 'success': False, 'message': error.message}, 400
