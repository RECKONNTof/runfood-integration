"""
Módulo para combinar datos de ventas con productos y formas de pago.

Provee funcionalidad para consolidar información de ventas, productos
y formas de pago en una estructura unificada.
"""

from typing import List, Dict, Any


def combine_sales_data(
    ventas_formas_pago: List[Dict[str, Any]], 
    ventas_productos: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Combina las formas de pago y productos en una estructura consolidada de ventas.
    
    Agrupa la información por número de comprobante (serie1, serie2, numero) y
    crea una estructura con la información general de la venta, detalles de 
    formas de pago y detalles de productos.
    
    Args:
        ventas_formas_pago: Lista con información general de ventas y formas de pago.
        ventas_productos: Lista con detalle de productos vendidos.
    
    Returns:
        List[Dict[str, Any]]: Lista de ventas consolidadas con todos los detalles.
    """
    ventas_consolidadas = {}
    
    # Iterar sobre las ventas del reporte de formas de pago
    for venta_forma_pago in ventas_formas_pago:
        # Genera el numero de factura
        invoice_number = f"{venta_forma_pago.get('serie1')}-{venta_forma_pago.get('serie2')}-{venta_forma_pago.get('numero')}"
        # Buscar si ya existe una venta consolidada con el mismo número y serie
        if invoice_number not in ventas_consolidadas:
            # Si no existe, crear un nuevo objeto de venta
            ventas_consolidadas[invoice_number] = {
                'cedula': venta_forma_pago.get('cedula'),
                'razonSocial': venta_forma_pago.get('razonSocial'),
                'telefono': venta_forma_pago.get('telefono'),
                'direccion': venta_forma_pago.get('direccion'),
                'claveAcceso': venta_forma_pago.get('claveAcceso'),
                'autorizacion': venta_forma_pago.get('autorizacion'),
                'fechaEmision': venta_forma_pago.get('fechaEmision'),
                'fechaAutorizacion': venta_forma_pago.get('fechaAutorizacion'),
                'numFactura': venta_forma_pago.get('numero'),
                'tipoComprobante': venta_forma_pago.get('idDocumento'),
                'total': venta_forma_pago.get('total'),
                'propina': venta_forma_pago.get('propina'),
                'descuentoTotal': venta_forma_pago.get('descuentoTotal'),
                'usuario': venta_forma_pago.get('Usuario'),
                'tipoIdentificacion': venta_forma_pago.get('TipoIdentificacion'),
                'numEstablecimiento': venta_forma_pago.get('serie1'),
                'numSerie': venta_forma_pago.get('serie2'),
                'numCorrelativo': venta_forma_pago.get('numero'),
                'detalleFp': [],
                'detalleVenta': []
            }
        
        # Añadir la forma de pago actual al detalle de formas de pago
        ventas_consolidadas[invoice_number]['detalleFp'].append({
            'tipoFormaPago': venta_forma_pago.get('FormaPago'),
            'numCheque': venta_forma_pago.get('numeroCheque'),
            'observacion': venta_forma_pago.get('observacion'),
            'tipoTarjeta': venta_forma_pago.get('TipoTarjeta'),
            'monto': venta_forma_pago.get('monto'),
            'marcaTarjeta': venta_forma_pago.get('MarcaTarjeta'),
            'bancoTarjeta': venta_forma_pago.get('BancoTarjeta')
        })
    
    # Iterar sobre los productos y asociarlos a la venta correspondiente
    for producto in ventas_productos:
        # Genera el numero de factura
        invoice_number = f"{producto.get('serie1')}-{producto.get('serie2')}-{producto.get('numero')}"
        venta_consolidada = ventas_consolidadas.get(invoice_number, None)
        
        # Si la venta existe, agregar el producto al detalleVenta
        if venta_consolidada:
            venta_consolidada['detalleVenta'].append({
                'codProducto': producto.get('codigo'),
                'descripcion': producto.get('descripcion'),
                'cantidad': producto.get('cantidad'),
                'precioUnitario': producto.get('pvp'),
                'porcentajeIva': producto.get('ivaPorcentaje'),
                'descuento': producto.get('descuento')
            })
    
    # Convertir el diccionario a una lista de ventas
    return list(ventas_consolidadas.values())
