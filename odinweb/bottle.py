"""
OdinWeb.Bottle API
~~~~~~~~~~~~~~~~~

Bottle implementation of the OdinWeb API interface.

Usage::
    
    import bottle
    from odinweb.bottle import Api
        
    app = bottle.Bottle()
    app.merge(
        Api(
            ApiVersion(
                UserApi(),
                version='v1
            )
        )
    )    

"""
from __future__ import absolute_import

from bottle import Route, response, request, BaseRequest

from odinweb.containers import ApiInterfaceBase
from odinweb.constants import Type, Method
from odinweb.data_structures import PathParam, MultiValueDict

TYPE_MAP = {
    Type.String: 're:[-_.\w\d]+',
    Type.Number: 'float',
    Type.Integer: 'int',
    Type.Boolean: 'bool',
    # Type.Array: 'list',
    # Type.File: 'string',
}


class RequestProxy(object):
    def __init__(self, r):
        # type: (BaseRequest) -> None
        self.scheme = r.urlparts.scheme
        self.host = r.urlparts.netloc
        self.path = r.urlparts.path
        self.GET = MultiValueDict(r.GET.allitems())
        self.headers = r.headers
        try:
            self.method = Method[r.method]
        except KeyError:
            self.method = None
        self.POST = MultiValueDict(r.POST.allitems())
        self.request = r

    @property
    def body(self):
        return self.request.body.read()


class Api(ApiInterfaceBase):
    def __iter__(self):
        """
        Convenience iterator to simplify registration with Bottle using :func:`bottle.Bottle.merge`. 
        """
        return self._build_routes()

    @staticmethod
    def node_formatter(path_node):
        # type: (PathParam) -> str
        """
        Format a node to be consumable by the `UrlPath.parse`.
        """
        if path_node.type:
            node_type = TYPE_MAP.get(path_node.type, 'str')
            if path_node.type_args:
                return "<{}:{}:{}>".format(path_node.name, node_type, ', '.join(path_node.type_args))
            return "<{}:{}>".format(path_node.name, node_type)
        return "<{}>".format(path_node.name)

    @property
    def plugins(self):
        # Placeholder to match the Bottle App API.
        return []

    def routes(self):
        return list(self._build_routes())

    def _bound_callback(self, operation):
        def callback(**path_args):
            resp = self.dispatch(operation, RequestProxy(request), **path_args)

            response.status = resp.status
            for k, v in resp.headers.items():
                response[k] = v

            return resp.body
        return callback

    def _build_routes(self):
        for url_path, operation in self.op_paths():
            path = url_path.format(self.node_formatter)
            for method in operation.methods:
                yield Route(self, path, method.value, self._bound_callback(operation))
