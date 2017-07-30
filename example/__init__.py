import odin

from bottle import Bottle
from odinweb import api, doc
from odinweb.bottle import Api
from odinweb.swagger import SwaggerSpec


class User(odin.Resource):
    """
    User resource
    """
    id = odin.IntegerField()
    username = odin.StringField()
    name = odin.StringField()
    email = odin.EmailField()
    role = odin.StringField(choices=('a', 'b', 'c'))

USERS = {
    1: User(1, 'pimpstar24', 'Bender', 'Rodreges', 'bender@ilovebender.com'),
    2: User(2, 'zoidberg', 'Zoidberg', '', 'zoidberg@freemail.web'),
    3: User(3, 'amylove79', 'Amy', 'Wong', 'awong79@marslink.web'),
}


class UserApi(api.ResourceApi):
    resource = User
    tags = ['user']

    @api.listing
    def get_user_list(self, request, offset, limit):
        return USERS[offset:limit], len(USERS)

    @api.create
    def create_user(self, request, user):
        global USERS

        # Add user to list
        user.id = len(USERS)
        USERS[user.id] = user

        return user

    @api.detail
    @doc.query_param('full', api.Type.Boolean)
    def get_user(self, request, resource_id):
        """
        Get a user object
        """
        user = USERS.get(resource_id)
        if not user:
            raise api.Error.from_status(api.HTTPStatus.NOT_FOUND)
        return user


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
