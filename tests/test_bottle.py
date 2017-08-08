from __future__ import absolute_import

import webtest

from bottle import Bottle, request

from odinweb import bottle
from odinweb.constants import Method
from odinweb.testing import check_request_proxy


def test_request_proxy():
    test_app = Bottle(catchall=False)
    app = webtest.TestApp(test_app)

    @test_app.route('/')
    def test_method():
        target = bottle.RequestProxy(request)
        check_request_proxy(target)
        assert target.method == Method.GET
        return 'OK'

    assert app.get('/?a=1&b=2&a=3', expect_errors=False).body == 'OK'
