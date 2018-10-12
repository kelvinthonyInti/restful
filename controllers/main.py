"""Part of odoo. See LICENSE file for full copyright and licensing details."""

import functools
import logging

from odoo import http
from odoo.addons.restful.common import valid_response, invalid_response, extract_arguments
from odoo.http import request

_logger = logging.getLogger(__name__)


def validate_token(func):
    """."""

    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        """."""
        access_token = request.httprequest.headers.get('access_token')
        if not access_token:
            return invalid_response('access_token_not_found', 'missing access token in request header', 401)
        access_token_data = request.env['api.access_token'].sudo().search(
            [('token', '=', access_token)], order='id DESC', limit=1)

        if access_token_data.find_one_or_create_token(user_id=access_token_data.user_id.id) != access_token:
            return invalid_response('access_token', 'token seems to have expired or invalid', 401)

        request.session.uid = access_token_data.user_id.id
        request.uid = access_token_data.user_id.id
        return func(self, *args, **kwargs)

    return wrap


"""
_routes = [
    '/api/<model>',
    '/api/<model>/<id>',
    '/api/<model>/<id>/<action>'
]
"""


class RestApi(http.Controller):
    """
    /api/auth                   POST    - Login in Odoo and set cookies

    /api/<model>                GET     - Read all (with optional domain, fields, offset, limit, order)
    /api/<model>/<id>           GET     - Read one (with optional fields)
    /api/<model>                POST    - Create one
    /api/<model>/<id>           PUT     - Update one
    /api/<model>/<id>           DELETE  - Delete one
    /api/<model>/<id>/<method>  PUT     - Call method (with optional parameters)
    """

    """
    Listar categoria de clientes. http://<ip>:<port>/api/res.partner.category
    """

    @validate_token
    @http.route('/api/kelvin.meza', type='http', auth='none', methods=["GET"], csrf=False)
    def search_read_res_partner_category(self):
        return "Kelvin Thony"


    @validate_token
    @http.route('/api/res.partner.category', type='http', auth='none', methods=["GET"], csrf=False)
    def search_read_res_partner_category(self):
        kwargs = {"fields": ["id", "name"]}
        # eval_request_params(kwargs)
        return request.env["res.partner.category"].search_read(**kwargs)

    """
    Listar Tipo de persona Sunat. http://<ip>:<port>/api/einvoice.catalog.type.person
    """

    @validate_token
    @http.route('/api/einvoice.catalog.type.person', auth='none', methods=["GET"], csrf=False)
    def search_read_einvoice_catalog_type_person(self):
        kwargs = {"fields": ["id", "code", "name"]}
        # eval_request_params(kwargs)
        return request.env["einvoice.catalog.type.person"].search_read(**kwargs)

    """
    Listar Tipo de documento Sunat. http://<ip>:<port>/api/einvoice.catalog.06
    """

    @validate_token
    @http.route('/api/einvoice.catalog.06', auth='none', methods=["GET"], csrf=False)
    def search_read_einvoice_catalog_06(self):
        kwargs = {"fields": ["id", "code", "name"]}
        # eval_request_params(kwargs)
        return request.env["einvoice.catalog.06"].search_read(**kwargs)

    """
    Listar Pais. http://<ip>:<port>/api/res.country
    """

    @validate_token
    @http.route('/api/res.country', auth='none', methods=["GET"], csrf=False)
    def search_read_res_country(self):
        kwargs = {"fields": ["id", "name", "code"]}
        # eval_request_params(kwargs)
        return request.env["res.country"].search_read(**kwargs)

    """
    Listar Departamentos. http://<ip>:<port>/api/res.country.state
    """

    @validate_token
    @http.route('/api/res.country.state', auth='none', methods=["GET"], csrf=False)
    def search_read_res_country_state(self):
        kwargs = {"fields": ["id", "country_id", "name", "code"]}
        # eval_request_params(kwargs)
        return request.env["res.country.state"].search_read(**kwargs)

    """
    Listar Provincias. http://<ip>:<port>/api/res.country.province
    """

    @validate_token
    @http.route('/api/res.country.province', auth='none', methods=["GET"], csrf=False)
    def search_read_res_country_province(self):
        kwargs = {"fields": ["id", "state_id", "name", "code"]}
        # eval_request_params(kwargs)
        return request.env["res.country.province"].search_read(**kwargs)

    """
    Listar distritos. http://<ip>:<port>/api/res.country.district
    """

    @validate_token
    @http.route('/api/res.country.district', auth='none', methods=["GET"], csrf=False)
    def search_read_res_country_district(self):
        kwargs = {"fields": ["id", "province_id", "name", "code"]}
        # eval_request_params(kwargs)
        return request.env["res.country.district"].search_read(**kwargs)

    """
    Listar Tipo de documento factura. http://<ip>:<port>/api/einvoice.catalog.01
    """

    @validate_token
    @http.route('/api/einvoice.catalog.01', auth='none', methods=["GET"], csrf=False)
    def search_read_einvoice_catalog_01(self):
        kwargs = {"fields": ["id", "code", "name", "type_operations_ids"]}
        # eval_request_params(kwargs)
        return request.env["einvoice.catalog.01"].search_read(**kwargs)

    """
    Listar Sucursal. http://<ip>:<port>/api/einvoice.branch.office
    """

    @validate_token
    @http.route('/api/einvoice.branch.office', auth='none', methods=["GET"], csrf=False)
    def search_read_einvoice_branch_office(self):
        kwargs = {"fields": ["id", "name", "description", "address", "district"]}
        # eval_request_params(kwargs)
        return request.env["einvoice.branch.office"].search_read(**kwargs)

    """
    FALTA 
    Listar Serie/Correlativo. http://<ip>:<port>/api/einvoice.series.correlative
    """

    @validate_token
    @http.route('/api/einvoice.series.correlative', auth='none', methods=["GET"], csrf=False)
    def search_read_einvoice_series_correlative(self):
        kwargs = {"fields": ["id", "description", "series", "correlative", "branch_office", "catalog_01_id"]}
        # eval_request_params(kwargs)
        return request.env["einvoice.series.correlative"].search_read(**kwargs)

    """
    Listar Cuenta para la venta. http://<ip>:<port>/api/account.account
    """

    @validate_token
    @http.route('/api/account.account', auth='none', methods=["GET"], csrf=False)
    def search_read_account_account(self):
        kwargs = {"fields": ["id", "name", "code"]}
        # eval_request_params(kwargs)
        return request.env["account.account"].search_read(**kwargs)

    """
    FALTA
    Listar productos. http://<ip>:<port>/api/product.template
    """

    @validate_token
    @http.route('/api/product.template', auth='none', methods=["GET"], csrf=False)
    def search_read_product_template(self):
        kwargs = {"fields": ["id", "name", "list_price", "standard_price", "categ_id", "taxes_id"]}
        # eval_request_params(kwargs)
        return request.env["product.template"].search_read(**kwargs)

    """
    Validar o crear clientes.
    """

    @validate_token
    @http.route('/api/create.validate.partner', auth='none',
                methods=["POST"], csrf=False)
    def create_validate_partner(self, **kwargs):
        # eval_request_params(kwargs)
        partner = request.env["res.partner"].search([("vat", "=", kwargs["vat"])])
        idPartner = False
        if len(partner) > 0:
            idPartner = partner.id
        else:
            idPartner = request.env["res.partner"].create(kwargs).id
        params = {"fields": ["id", "name", "vat", "mobile", "email", "category_id"]}
        result = request.env["res.partner"].browse(idPartner).read(**params)
        return result and result[0] or {}

    """
    Listar el equipo de mesa. http://<ip>:<port>/api/helpdesk.team
    """

    @validate_token
    @http.route('/api/helpdesk.team', auth='none', methods=["GET"], csrf=False)
    def search_read_helpdesk_team(self):
        kwargs = {"fields": ["id", "name"], "domain": [('it_is_support', '=', True)]}
        # eval_request_params(kwargs)
        return request.env["helpdesk.team"].search_read(**kwargs)

    """
    Listar etiquetas de ticket. http://<ip>:<port>/api/helpdesk.tag
    """

    @validate_token
    @http.route('/api/helpdesk.tag', auth='none', methods=["GET"], csrf=False)
    def search_read_helpdesk_tag(self):
        kwargs = {"fields": ["id", "name", "it_invited_ids"]}
        # eval_request_params(kwargs)
        return request.env["helpdesk.tag"].search_read(**kwargs)

    """
    Listar tipos de ticket. http://<ip>:<port>/api/helpdesk.ticket.type
    """

    @validate_token
    @http.route('/api/helpdesk.ticket.type', auth='none', methods=["GET"], csrf=False)
    def search_read_helpdesk_ticket_type(self):
        kwargs = {"fields": ["id", "name"]}
        # eval_request_params(kwargs)
        return request.env["helpdesk.ticket.type"].search_read(**kwargs)

    """
    Listar tipos de origen. http://<ip>:<port>/api/it.ticket.origin
    """

    @validate_token
    @http.route('/api/it.ticket.origin', auth='none', methods=["GET"], csrf=False)
    def search_read_it_ticket_origin(self):
        kwargs = {"fields": ["id", "it_name", "it_code"]}
        # eval_request_params(kwargs)
        return request.env["it.ticket.origin"].search_read(**kwargs)

    """
    Listar prioridad de ticket. http://<ip>:<port>/api/ticket.priority
    """

    @validate_token
    @http.route('/api/ticket.priority', auth='none', methods=["GET"], csrf=False)
    def search_priority(self):
        array_priority = [
            {
                'code': "0",
                'description': 'Todos'

            },
            {
                'code': "1",
                'description': 'Prioridad baja'

            },
            {
                'code': "2",
                'description': 'Alta prioridad'
            },

            {
                'code': "3",
                'description': 'Urgente'
            }
        ]
        return array_priority

    """
    Listar clientes. http://<ip>:<port>/api/res.partner
    """

    @validate_token
    @http.route('/api/res.partner', auth='none', methods=["GET"], csrf=False)
    def search_read_res_partner(self):
        kwargs = {
            "fields": ["id", "name", "firstname", "lastname", "lastname2", "vat", "street", "phone", "email", "mobile",
                       "category_id"]}
        # eval_request_params(kwargs)
        return request.env["res.partner"].search_read(**kwargs)

    """
    Listar usuarios. http://<ip>:<port>/api/res.users
    """

    @validate_token
    @http.route('/api/res.users', auth='none', methods=["GET"], csrf=False)
    def search_read_res_users(self):
        kwargs = {"fields": ["id", "email", "partner_id", "name", "login"], "domain": [('id', '!=', 1)]}
        # eval_request_params(kwargs)
        return request.env["res.users"].search_read(**kwargs)

    """
    Crear helpdesk ticket. http://<ip>:<port>/api/helpdesk.ticket
    """

    @validate_token
    @http.route('/api/helpdesk.ticket', auth='none',
                methods=["POST"], csrf=False)
    def create_helpdesk_ticket(self, **kwargs):
        # eval_request_params(kwargs)
        ticket_id = request.env["helpdesk.ticket"].create(kwargs)
        if ticket_id.id is not False:
            tag_ids = ticket_id.tag_ids
            for tag in tag_ids:
                for follower in tag.it_invited_ids:
                    vals_wizard_invite = {
                        "partner_ids": [(4, follower.id)],
                        "send_mail": True,
                        "res_model": "helpdesk.ticket",
                        "res_id": ticket_id.id
                    }
                    wizart_invite = request.env["mail.wizard.invite"].create(vals_wizard_invite)
                    wizart_invite.add_followers()
            return ticket_id.id
        else:
            return 0

    """
    CREAR FACTURAS
    """

    """
    Crear Facturas. http://<ip>:<port>/api/account.invoice
    """

    @validate_token
    @http.route('/api/account.invoice', auth='none',
                methods=["POST"], csrf=False)
    def create_account_invoice(self, **kwargs):
        # eval_request_params(kwargs)
        account_invoice_id = request.env["account.invoice"].create(kwargs)
        if account_invoice_id.id is not False:
            for item in kwargs["invoice_lines"]:
                item["invoice_id"] = account_invoice_id.id
                invoice_line_id = request.env["account.invoice.line"].create(item)
        return kwargs

    """
    REGISTRAR PAGOS
    """
    """
    Registrar pagos. http://<ip>:<port>/api/account.payment
    """

    @validate_token
    @http.route('/api/account.journal', auth='none', methods=["GET"], csrf=False)
    def search_account_payment(self):
        kwargs = {
            "fields": ["id", "name"]}
        # eval_request_params(kwargs)
        return request.env["account.journal"].search_read(**kwargs)

    @validate_token
    @http.route('/api/account.payment', auth='none',
                methods=["POST"], csrf=False)
    def account_payment(self, **kwargs):
        # eval_request_params(kwargs)
        if 'invoice_id' in kwargs:
            account_id = request.env["account.invoice"].browse(kwargs["invoice_id"])
            payment_method_id = request.env["account.payment.method"].search(
                [('code', '=', 'manual'), ('payment_type', '=', 'inbound')])
            payment_id = request.env["account.payment"].create({
                'amount': kwargs["amount"],
                'journal_id': kwargs["journal_id"],
                'payment_date': kwargs["payment_date"],
                'it_detraccion': kwargs["it_detraccion"],
                'it_date': kwargs["it_date"],
                'communication': account_id.number,
                'payment_type': "inbound",
                'partner_type ': "customer",
                'payment_method_id': payment_method_id.id,
                'it_comprobante': kwargs["it_comprobante"],
                'invoice_ids': [(4, account_id.id)]
            })
            payment_id.write({'partner_type': "customer"})
            payment_id.action_validate_invoice_payment()
            return payment_id.id
        else:
            return False

    """
    Validar o crear clientes / Crear Ticket.
    """

    @validate_token
    @http.route('/api/create.partner.ticket', auth='none',
                methods=["POST"], csrf=False)
    def create_partner_ticket(self, **kwargs):
        # eval_request_params(kwargs)
        partner = request.env["res.partner"].search([("email", "=", kwargs["email"])])
        idPartner = False
        if len(partner) > 0:
            idPartner = partner.id
        else:
            params_partner = {
                'email': kwargs["email"],
                'lastname': kwargs["lastname"],
                'lastname2': kwargs["lastname2"],
                'firstname': kwargs["firstname"]
            }
            idPartner = request.env["res.partner"].create(params_partner).id
        if idPartner is not False:

            params_ticket = {
                'name': kwargs["name"],
                'description': kwargs["description"],
                'team_id': kwargs["team_id"],
                'partner_id': idPartner,
                'ticket_type_id': kwargs["ticket_type_id"],
                'tag_ids': kwargs["tag_ids"],
                'it_origin': kwargs["it_origin"],
                'priority': kwargs["priority"]
            }
            ticket_id = request.env["helpdesk.ticket"].create(params_ticket)
            if ticket_id.id is not False:
                tag_ids = ticket_id.tag_ids
                for tag in tag_ids:
                    for follower in tag.it_invited_ids:
                        vals_wizard_invite = {
                            "partner_ids": [(4, follower.id)],
                            "send_mail": True,
                            "res_model": "helpdesk.ticket",
                            "res_id": ticket_id.id
                        }
                        wizart_invite = request.env["mail.wizard.invite"].create(vals_wizard_invite)
                        wizart_invite.add_followers()
                return ticket_id.id
            else:
                return 0
        else:
            return 0

