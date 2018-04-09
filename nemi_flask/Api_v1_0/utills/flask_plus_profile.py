from flask_restplus import Namespace
from flask_restplus.model import Model, Draft4Validator, ValidationError
from flask_restplus.reqparse import Argument
import six

from .response_init import ProfileError


class ModelProfile(Model):

    def validate(self, data, resolver=None, format_checker=None):
        validator = Draft4Validator(self.__schema__, resolver=resolver, format_checker=format_checker)
        try:
            validator.validate(data)
        except ValidationError:
            raise ProfileError(code=400, message=dict(self.format_error(e) for e in validator.iter_errors(data)))


class NamespaceProfile(Namespace):

    def model(self, name=None, model=None, mask=None, **kwargs):
        model = ModelProfile(name, model, mask=mask)
        model.__apidoc__.update(kwargs)
        return self.add_model(name, model)


class ArgumentProfile(Argument):

    def handle_validation_error(self, error, bundle_errors):
        error_str = six.text_type(error)
        errors = {self.name: error_str}
        if bundle_errors:
            return error, errors
        raise ProfileError(code=400, message=errors)
