import odin

from bottle import Bottle
from odinweb import api, doc
from odinweb.bottle import Api
from odinweb.swagger import SwaggerSpec

app = Bottle()


class User(odin.Resource):
    id = odin.IntegerField()
    name = odin.StringField()


class UserApi(api.ResourceApi):
    resource = User

    @api.listing
    def get_user_list(self, request, limit, offset):
        return [
            User(1, "tim"),
            User(2, "sara"),
        ], 2

    @api.create
    @doc.response(201, 'Return added user.', User)
    def create_user(self, request):
        pass

    @api.detail
    @doc.operation(tags=['user'])
    @doc.parameter('full', api.IN_QUERY, type_=api.TYPE_BOOLEAN)
    @doc.response(200, 'Return requested user.', User)
    def get_user(self, request, resource_id):
        """
        Get a user object
        """
        return User(resource_id, "tim")

    @api.update
    def update_user(self, request, resource_id):
        pass


app.merge(
    Api(
        api.ApiVersion(
            SwaggerSpec(title="Bottle API Swagger"),
            UserApi(),
        ),
        debug_enabled=True
    )
)
