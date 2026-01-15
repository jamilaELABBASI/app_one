from odoo import http


class TestApi(http.Controller):
    # type (http ou jsoon)
    @http.route(['/api/test'],methods=["GET"], type='http', auth='none',csrf=False)
    def test_endpoint(self):
        print()
