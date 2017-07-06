import odin

from bottle import Bottle
from odinweb.api import ResourceApi, ApiCollection
from odinweb.bottle import Api
from odinweb.data_structures import ApiRoute, PathNode

app = Bottle()


class Book(odin.Resource):
    title = odin.StringField()
    published = odin.DateField()
    authors = odin.TypedListField(odin.StringField())


class BookApi(ResourceApi):
    resource = Book


@app.route("/<name>/")
def hello(name):
    return "HelloWorld! " + name


def sample_callback(request, **kwargs):
    return "Response: {}\n{}\n{}".format(request.path, kwargs, request.method)


app.merge(
    Api(
        ApiCollection(
            ApiRoute(1, ['user'], ['GET', 'POST'], sample_callback),
            ApiRoute(1, ['user', PathNode('resource_id', 'int', [])], ['GET', 'POST'], sample_callback),
        ),
        # ApiVersion(BookApi)
    )
)
