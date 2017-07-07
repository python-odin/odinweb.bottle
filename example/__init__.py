import odin

from bottle import Bottle
from odinweb.api import ResourceApi, ApiVersion, detail, listing
from odinweb.bottle import Api

app = Bottle()


class User(odin.Resource):
    id = odin.IntegerField()
    name = odin.StringField()


class UserApi(ResourceApi):
    resource = User

    @listing
    def get_user_list(self, request, limit, offset):
        return [
            User(1, "tim"),
            User(2, "sara"),
        ], 2

    @detail
    def get_user(self, request, resource_id):
        return User(resource_id, "tim")


app.merge(
    Api(
        ApiVersion(
            UserApi()
        ),
        debug_enabled=True
    )
)
