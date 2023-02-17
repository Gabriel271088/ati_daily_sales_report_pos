# -*- coding: utf-8 -*-
import logging 
from datetime import timedelta
from datetime import datetime
from odoo import models, fields, api, exceptions, _
 
_logger = logging.getLogger(__name__)

class ProductWizard(models.TransientModel):
    _name = 'ati.sale.report.wizard'
 
 
    start_date = fields.Datetime("Fecha inicio")
    end_date = fields.Datetime("Fecha fin")
    
    @api.multi
    def get_pdf_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'start_date': self.start_date,
                'end_date': self.end_date,
            }
        }
        return self.env.ref('ati_daily_sales_report_pos.pos_daily_report').report_action(self, data=data)

class ReportPosDailyRecap(models.AbstractModel):
    _name = 'report.ati_daily_sales_report_pos.report_ati_daily_sale'

    @api.model
    def get_report_values(self, docids, data=None):
        date_start = data['form']['start_date']
        date_end = data['form']['end_date']

        pedidos = self.env['pos.order'].search([('date_order','>=',str(datetime.strptime(date_start,'%Y-%m-%d %H:%M:%S') + timedelta(hours=3))),('date_order','<=', str(datetime.strptime(date_end,'%Y-%m-%d %H:%M:%S') + timedelta(hours=3)))])
        _categories = []
        _existing_categories = []
        _total_ventas = 0
        for p in pedidos:
            for lp in p.statement_ids:
                _logger.warning('***** Pedido: {0} pago: {1} con monto: {2}'.format(p.name, lp.journal_id.name, lp.amount))

                # Si la categoria aun no se a detectado se agrega por primera vez y se cargan 
                # los totales de la linea que contiene el producto de la nueva categoria
                if not lp.journal_id.name in _existing_categories:
                    _vals={'categoria' : lp.journal_id.name,
                            'total': lp.amount}
                    _categories.append(_vals)
                    _existing_categories.append(lp.journal_id.name)
                # En el caso de que ya se haya cargado la categoria se suman los totales del producto de dicha categoria
                else:
                    for cate in _categories:
                        if cate['categoria'] == lp.journal_id.name:
                            cate['total'] = cate['total'] + lp.amount
        for c in _categories:
            _total_ventas += c['total']

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'categories': _categories,
            'total_ventas': _total_ventas,
            'cant_ventas': len(pedidos)
        }
