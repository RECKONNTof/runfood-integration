"""
Controlador principal para la integración de ventas.

Maneja la lógica de negocio para obtener, procesar y consolidar
datos de ventas desde RunFood.
"""

import json
from typing import Optional, Dict, Any
from ..services import (
    get_products_from_sales, 
    get_payment_from_sales,
    process_items,
    combine_sales_data
)
from ..core.make_http_request import make_http_request
from ..core.get_env_variables import EnvVariables


def get_and_process_sales(start_date: str, end_date: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene y procesa las ventas combinando información de productos y formas de pago.
    
    Args:
        start_date: Fecha de inicio para filtrar las ventas (formato YYYY-MM-DD).
        end_date: Fecha de fin para filtrar las ventas (formato YYYY-MM-DD).
    
    Returns:
        Optional[Dict[str, Any]]: Datos consolidados de ventas o mensaje de error.
    """
    try:
        print("Obteniendo datos de productos de RunFood...")
        productos = get_products_from_sales(start_date, end_date)
        
        print("Obteniendo datos de formas de pago de RunFood...")
        formas_pago = get_payment_from_sales(start_date, end_date)
        
        # Verificar si ambas respuestas tienen datos
        if productos and formas_pago:
            # Procesar los datos eliminando campos innecesarios
            processed_productos = process_items(productos)
            processed_formas_pago = process_items(formas_pago)
            
            # Combinar los datos de ventas, formas de pago y productos
            ventas_agrupadas = combine_sales_data(
                ventas_formas_pago=processed_formas_pago,
                ventas_productos=processed_productos
            )
            
            print("Datos combinados correctamente")
            return ventas_agrupadas
        else:
            # Retornar un objeto indicando que no se recibieron datos
            error_data = {
                "status": "error",
                "message": "No se recibieron datos de una o ambas APIs de RunFood",
                "fecha_desde": start_date,
                "fecha_hasta": end_date
            }
            print("No se obtuvieron datos completos, se generará un mensaje de error")
            return error_data
            
    except Exception as e:
        print(f"Error al obtener y procesar las ventas: {e}")
        return {
            "status": "error",
            "message": f"Error en el procesamiento: {str(e)}",
            "fecha_desde": start_date,
            "fecha_hasta": end_date
        }


def send_sales_to_server(
    start_date: str,
    end_date: str,
    sales_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
    """
    Envía los datos consolidados de ventas al servidor Reckonnt.
    
    Args:
        start_date: Fecha de inicio del rango de ventas.
        end_date: Fecha de fin del rango de ventas.
        sales_data: Datos de ventas consolidados a enviar.
    
    Returns:
        Optional[Dict[str, Any]]: Respuesta del servidor o None en caso de error.
    """
    try:
        # Obtener la URL del servidor desde las variables de entorno
        server_url = EnvVariables.get_variable("RECKONNT_SALE_API_URL")
        token = EnvVariables.get_variable("TOKEN")
        url = server_url.replace('__fecha_desde__', start_date).replace('__fecha_hasta__', end_date).replace('__token__', token)
        # Configurar las cabeceras
        headers = {
            "Content-Type": "application/json",
            "Accept": "/",
            "Host": "reckonnt.net"
        }
        
        # Enviar los datos al servidor
        print("Enviando datos al servidor...")
        response = make_http_request(
            url=url,
            method="POST",
            data=sales_data,
            headers=headers
        )
        
        if response:
            print(f"Respuesta del servidor: {json.dumps(response, indent=2, ensure_ascii=False)}")
            return response
        else:
            print("Error al enviar los datos al servidor.")
            return None
            
    except Exception as e:
        print(f"Error al enviar datos al servidor: {e}")
        return None
