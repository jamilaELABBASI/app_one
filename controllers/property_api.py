import json
import math
from urllib.parse import parse_qs
from odoo import http
from odoo.http import request


def valid_response(data,status,pagination_infos):
    response_body={
        'message': 'succesful',
        'data':data,
    }
    if pagination_infos:
        response_body['pagination_infos'] = pagination_infos
    return request.make_json_response(response_body,status=status)

def invalid_response(error,status):
    response_body={
        'message':error
    }
    return request.make_json_response(response_body,status=status)


class PropertyApi(http.Controller):
    # @http.route(['/property/create'], methods=["POST"], type='http', auth='none', csrf=False)
    # def create_property(self):
    #     #print('inside post_property method')
    #     args=request.httprequest.data.decode()
    #     vals = json.loads(args)
    #     #print(vals)
    #     if not vals.get('name'):
    #         return request.make_json_response({
    #             "message": " field name is required you can't create property wiithout it"
    #         }, status=400)
    #     try:
    #         res = request.env['property'].sudo().create(vals)
    #         # print(res)
    #         if res:
    #             return request.make_json_response({
    #                 "message": "property has been created successfully"
    #             }, status=201)  # 201 status code qui dit que la creation est faite avec succes
    #     except Exception as e:
    #         return request.make_json_response({
    #             "message": "error"
    #         }, status=400)

    @http.route(['/property/create'], methods=["POST"], type='http', auth='none', csrf=False)
    def create_property(self):
        # print('inside post_property method')
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        # print(vals)
        if not vals.get('name'):
            return request.make_json_response({
                "message": " field name is required you can't create property wiithout it"
            }, status=400)
        try:
            # res = request.env['property'].sudo().create(vals)
            # print(res)
            cr=request.env.cr
            columns=','.join(vals.keys()) # name , postcode
            values=','.join(['%s']*len(vals))#
            query=f"""INSERT INTO property ({columns}) VALUES ({values}) RETURNING id,name,postcode"""
            cr.execute(query,tuple(vals.values()))
            # query="INSERT INTO property (name,postcode) VALUES ('property 1 from query','123') RETURNING id,name,postcode"
            # cr.execute(query,tuple(vals.values()))
            res=cr.fetchone()
            if res:
                return request.make_json_response({
                    "id": res[0],
                    "name": res[1],
                    "postcode": res[2],
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
            # ou property_rec = request.env['property'].search([('id', '=', property_id)], limit=1)
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

    @http.route(['/property/read/<int:property_id>'], methods=["GET"], type='http', auth='public', csrf=False)
    def read_property(self,property_id):
        try:
            property_rec = request.env['property'].sudo().browse(property_id)
            # return property_rec
            if not property_rec.exists():
                return request.make_json_response({" property with this id not existe"},status=404)
            return request.make_json_response(property_rec.read()[0],status=200) # on peut recuperer specifiques  attributs { property_rec.name} etc """
        except Exception as e:
            return request.make_json_response({
                    'message':'error'
                }, status=200)


    @http.route(['/property/all'], methods=["GET"], type='http', auth='public', csrf=False)
    def all_property(self):
        try:
            properties = request.env['property'].sudo().search([])

            if not properties:
                return request.make_json_response({
                    "count": 0,
                    "properties": []
                }, status=200)

            data = [{
                "id": prop.id,
                "name": prop.name,
                "postcode": prop.postcode,
                "state": prop.state,
            } for prop in properties]

            return request.make_json_response({
                "count": len(data),
                "properties": data
            }, status=200)

        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)

    @http.route(['/property/list/filter'], methods=["GET"], type='http', auth='public', csrf=False)
    def all_property_filter(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))

            domain = []

            # valeurs par défaut
            limit = 5
            page = 1

            if params.get('limit'):
                limit = int(params['limit'][0])

            if params.get('page'):
                page = int(params['page'][0])
                if page < 1:
                    page = 1

            # calcul correct du offset
            offset = (page - 1) * limit

            if params.get('state'):
                domain.append(('state', '=', params['state'][0]))

            Property = request.env['property'].sudo()

            property_ids = Property.search(domain, offset=offset, limit=limit, order='id DESC')
            property_count = Property.search_count(domain)

            data = [{
                "id": prop.id,
                "name": prop.name,
                "postcode": prop.postcode,
                "state": prop.state,
            } for prop in property_ids]

            return request.make_json_response({
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "pages": math.ceil(property_count / limit) if limit else 1,
                    "count": property_count,
                },
                "data": data
            }, status=200)
        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)

    # @http.route(['/property/all'],methods=['GET'],type='http',auth='public',csrf=False)
    # def all_property(self):
    #     try:
    #         properties_ids=request.env['property'].sudo().search([])
    #         if properties_ids:
    #             return request.make_json_response({
    #                 "name":property_id.name for property_id in properties_ids
    #             },status=200)
    #         else:
    #             return request.make_json_response({
    #                 'message':'error'
    #             })
    #     except Exception as e:
    #         return request.make_json_response({
    #             'message':e
    #         })

    @http.route(['/property/delete/<int:property_id>'], methods=["DELETE"], type='http', auth='public', csrf=False)
    def delete_property(self, property_id):
        property_rec = request.env['property'].sudo().browse(property_id)
        if not property_rec.exists():
            return request.make_json_response({
                "message": " property with this id not existe"
            }, status=400)
        else:
            property_rec.unlink()
            return request.make_json_response({
                "message": "property has been deleted successfully"
            }, status=200)
