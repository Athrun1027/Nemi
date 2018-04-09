from flask import Blueprint
from flask_restplus import Api

from .namespace_auth.views import api as api_auth
from .namespace_users.views import api as api_users
from .namespace_spaces.views import api as api_spaces
from .namespace_folders.views import api as api_folders
from .namespace_files.views import api as api_files
from .namespace_buckets.views import api as api_buckets
from .namespace_groups.views import api as api_groups
from .namespace_resources.views import api as api_resources
from .namespace_tags.views import api as api_tags
from .namespace_search.views import api as api_search
from .namespace_message.views import api as api_message
from .namespace_share.views import api as api_share
from .namespace_logs.views import api as api_logs

# init the blueprint
blueprint = Blueprint('v1', __name__)

# define authorizations
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Nemi-API-KEY'
    }
}

# init the restful api
api_blueprint = Api(
    blueprint,
    title='Nemi Api v1.0',
    version='1.0',
    description='记得喝水',
    authorizations=authorizations,
    security='apikey'
)

# add all namespaces in here
api_blueprint.add_namespace(api_auth)
api_blueprint.add_namespace(api_users)
api_blueprint.add_namespace(api_spaces)
api_blueprint.add_namespace(api_folders)
api_blueprint.add_namespace(api_files)
api_blueprint.add_namespace(api_buckets)
# api_blueprint.add_namespace(api_upload)
api_blueprint.add_namespace(api_resources)
api_blueprint.add_namespace(api_tags)
api_blueprint.add_namespace(api_search)
api_blueprint.add_namespace(api_message)
api_blueprint.add_namespace(api_groups)
api_blueprint.add_namespace(api_share)
api_blueprint.add_namespace(api_logs)
