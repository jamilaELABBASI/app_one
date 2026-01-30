from ast import literal_eval
from odoo import http
from odoo.http import request
import io
import xlsxwriter


class XlsxPropertyReport(http.Controller):

    @http.route('/property/excel/report/<string:property_ids>', type='http', auth='user', csrf=False)
    def download_property_excel_report(self, property_ids):

        # 1️⃣ Convert string to list
        property_ids = literal_eval(property_ids)

        # 2️⃣ Convert IDs to RECORDSET (CRITICAL)
        properties = request.env['property'].browse(property_ids)

        # 3️⃣ Excel setup
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Properties')

        header_format = workbook.add_format({
            'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'
        })
        body_format = workbook.add_format({'align': 'center'})
        price_format = workbook.add_format({'num_format': '##,##00.00$', 'border': 1, 'align': 'center'})

        headers = ['Name', 'Postcode', 'Selling price', 'Garden']

        # 4️⃣ Write headers (ONLY headers here)
        for num_column, header in enumerate(headers):
            worksheet.write(0, num_column, header, header_format)

        # 5️⃣ Write data (ONLY records here)
        row = 1
        for prop in properties:
            worksheet.write(row, 0, prop.name or '', body_format)
            worksheet.write(row, 1, prop.postcode or '', body_format)
            worksheet.write(row, 2, prop.selling_price or 0,price_format)
            worksheet.write(row, 3, 'Yes' if prop.garden else 'No', body_format)
            row += 1

        workbook.close()
        output.seek(0)

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename=Property_Report.xlsx')
            ]
        )
