from odoo import http


class PropertyApi(http.Controller):
    @http.route(['/property'], methods=["POST"], type='http', auth='public', csrf=False)
    def post_property(self):
        print('inside post_property method')


"""
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class PropertyApi(http.Controller):

    @http.route('/property', type='http', auth='none', methods=['POST', 'GET'], csrf=False)
    def post_property(self, **kwargs):
        _logger.info("✅ MESSAGE BACKEND : endpoint /property appelé")
        return "OK"


"""
