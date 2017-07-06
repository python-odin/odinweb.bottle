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
    def get_user_list(self):
        return [
            User(1, "tim"),
            User(2, "sara"),
        ]

    @detail
    def get_user(self, resource_id):
        return User(1, "tim")


@app.route("/<name>/")
def hello(name):
    return "HelloWorld! " + name


def sample_callback(request, **kwargs):
    return "Response: {}\n{}\n{}".format(request.path, kwargs, request.method)

app.merge(
    Api(
        ApiVersion(
            UserApi()
        )
    )
)
