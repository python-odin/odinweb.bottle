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

from bottle import Route, response, request
from odinweb.data_structures import PathNode, ApiBase


class Api(ApiBase):
    def __iter__(self):
        """
        Convenience iterator to simplify registration with Bottle using :func:`bottle.Bottle.merge`. 
        """
        return iter(self.routes())

    @property
    def plugins(self):
        # Placeholder to match the Bottle App API.
        return []

    def routes(self):
        return list(self._build_routes())

    def parse_node(self, node):
        if isinstance(node, PathNode):
            if node.type_args:
                return "<{}:{}({})>".format(node.name, node.type, ', '.join(node.type_args))
            else:
                return "<{}:{}>".format(node.name, node.type)
        else:
            return str(node)

    def _build_routes(self):
        for path, methods, callback in super(Api, self)._build_routes():
            callback = self._bound_callback(callback)
            for method in methods:
                yield Route(self, path, method, callback)

    def _bound_callback(self, f):
        def callback(**kwargs):
            resp = f(request, **kwargs)

            # Todo: Deal with response object and map back to Bottle.response
            response.add_header('content-type', 'text/plain')

            return resp
        return callback
