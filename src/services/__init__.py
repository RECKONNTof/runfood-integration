"""
Módulo Services con funciones para interactuar con locales y externos.
- Locales: Runfood
- Externos: Reckonnt

Provee funcionalidad para consultar información de ventas y productos.
"""
from .get_sales_payment_detail import get_payment_from_sales
from .get_sales_product_detail import get_products_from_sales
from .process_sales_data import process_items, remove_unwanted_fields
from .combine_sales_data import combine_sales_data

__all__ = [
    'get_products_from_sales',
    'get_payment_from_sales',
    'process_items',
    'remove_unwanted_fields',
    'combine_sales_data'
]
