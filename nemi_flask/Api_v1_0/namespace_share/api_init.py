from werkzeug.datastructures import FileStorage
from flask_restplus import fields, reqparse


from ..utills.response_init import ProfileError
from ..utills.flask_plus_profile import NamespaceProfile as Namespace, ArgumentProfile


api = Namespace('shares', description='分享模块')


@api.errorhandler(ProfileError)
def profile_error(error):
    return {'code': error.code, 'success': False, 'message': error.message}, 400
