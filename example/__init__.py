import odin

from bottle import Bottle
from odinweb import api, doc
from odinweb.bottle import Api
from odinweb.swagger import SwaggerSpec


class User(odin.Resource):
    id = odin.IntegerField()
    name = odin.StringField()
    role = odin.StringField(choices=('a', 'b', 'c'))


class UserApi(api.ResourceApi):
    resource = User
    tags = ['user']

    @api.listing
    def get_user_list(self, request, limit, offset):
        return [
            User(1, "tim"),
            User(2, "sara"),
        ], 2

    @api.create
    def create_user(self, request, user):
        user.id = 3
        return user

    @api.detail
    @doc.query_param('full', api.Type.Boolean)
    def get_user(self, request, resource_id):
        """
        Get a user object
        """
        return User(resource_id, "tim")


app = Bottle()
app.merge(
    Api(
        api.ApiVersion(
            SwaggerSpec(title="Bottle API Swagger", enable_ui=True),
            UserApi(),
        ),
        debug_enabled=True
    )
)
