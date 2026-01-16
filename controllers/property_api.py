import json
from odoo import http
from odoo.http import request


class PropertyApi(http.Controller):
    @http.route(['/property/create'], methods=["POST"], type='http', auth='none', csrf=False)
    def create_property(self):
        #print('inside post_property method')
        args=request.httprequest.data.decode()
        vals = json.loads(args)
        #print(vals)
        if not vals.get('name'):
            return request.make_json_response({
                "message": " field name is required you can't create property wiithout it"
            }, status=400)
        try:
            res = request.env['property'].sudo().create(vals)
            # print(res)
            if res:
                return request.make_json_response({
                    "message": "property has been created successfully"
                }, status=201)  # 201 status code qui dit que la creation est faite avec succes
        except Exception as e: 
            return request.make_json_response({
                "message": "error"
            }, status=400)

    @http.route(['/property/update/<int:property_id>'], methods=["PUT"], type='http', auth='none', csrf=False)
    def update_property(self,property_id):
        try:
            if not property_id:
                return request.make_json_response({
                    "message": " property with this id not existe"
                },status=400)
            property_rec = request.env['property'].sudo().browse(property_id)
            # ou si on utilise type=json property_rec = request.env['property'].browse(property_id)
            print("PROPERTY ID =", property_id)
            vals = json.loads(request.httprequest.data)
            property_rec.write(vals)
            return request.make_json_response({
                "message": "property has been updated successfully",
                "property_id": property_id,
                "property_name": property_rec.name
            },status=200)
        except Exception as e:
            return request.make_json_response({
                "message": "error"
            },status=400)




