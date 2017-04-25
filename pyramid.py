# -*- coding: utf-8 -*-

# Sample Of Pyramid Based ZarinPal WebGate
# Based On ZarinPAl Sample Flask Code: https://github.com/ZarinPal-Lab/SampleCode-Python-Flask/

__author__ = 'Mohammad Sadegh Alirezaie'
__url__ = 'webgo.ir'
__license__ = 'MIT https://opensource.org/licenses/MIT'

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.request import Request
from pyramid.httpexceptions import HTTPFound
from suds.client import Client

MMERCHANT_ID = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'  # Required
ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
amount = 1000  # Amount will be based on Toman  Required
description = u'توضیحات تراکنش تستی'  # Required
email = 'user@userurl.ir'  # Optional
mobile = '09123456789'  # Optional

@view_config(route_name='payment', renderer='string')
def payment(request):
    client = Client(ZARINPAL_WEBSERVICE)
    result= client.service.PaymentRequest(MMERCHANT_ID,
                    amount,
                    description,
                    email,
                    mobile,
                    str(request.static_url('verify')))

    if result.Status == 100:
        return HTTPFound('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
    else:
        return 'Error!'

@view_config(route_name='verify', renderer='string')
def verify(request):
    client = Client(ZARINPAL_WEBSERVICE)

    if request.GET['Status'] == 100:
        result = client.PaymentVerification(MMERCHANT_ID, request.params['Authority'], amount)

        if result.Status == 100:
            return 'Transaction success. RefID: ' + str(result.RefID))
        elif result.status == 101:
            return 'Transaction submitted : ' + str(result.Status)
        else:
            return 'Transaction failed. Status: ' + str(result.Status)

    return 'Transaction failed or canceled by user'

if __name__ == '__main__':
    config = Configurator()
    config.add_route('payment', '/payment')
    config.add_route('verify', '/verify')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
