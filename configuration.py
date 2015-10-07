# This file is part of the stock_shipment_cashondelivery module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields, ModelSQL, ModelView
from trytond.pool import PoolMeta
from trytond.transaction import Transaction
from trytond import backend

__all__ = ['ConfigurationSalePaymentType', 'Configuration']
__metaclass__ = PoolMeta


class ConfigurationSalePaymentType(ModelSQL, ModelView):
    'Configuration - Sale Payment Type'
    __name__ = 'sale.configuration-sale.payment.type'
    _table = 'sale_configuration_sale_payment_type'
    sale_configuration = fields.Many2One('sale.configuration',
        'Sale Configuration', ondelete='CASCADE', select=True)
    payment_type = fields.Many2One('account.payment.type', 'Payment Type',
        ondelete='RESTRICT', select=True, required=True)

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        cursor = Transaction().cursor

        # Migration from 3.6: rename table
        old_table = 'sale_configuration_sale_payment_type_rel'
        new_table = 'sale_configuration_sale_payment_type'
        if TableHandler.table_exist(cursor, old_table):
            TableHandler.table_rename(cursor, old_table, new_table)


class Configuration:
    __name__ = 'sale.configuration'
    cashondelivery_payments = fields.Many2Many(
        'sale.configuration-sale.payment.type', 'sale_configuration',
        'payment_type', 'Cash on Delivery Payment Types',
        domain=[('kind', '=', 'receivable')],
        )
