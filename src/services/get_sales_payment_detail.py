"""
Módulo para obtener detalles de productos en ventas.

Provee funcionalidad para consultar información detallada de productos
desde la API de ventas.
"""

from typing import Optional
from ..core.make_http_request import make_http_request
from ..core.get_env_variables import EnvVariables


def get_payment_from_sales(start_date: str, end_date: str) -> Optional[dict]:
    """
    Obtiene los productos facturados dentro de un rango de fechas especificado.
    
    Args:
        start_date: Fecha de inicio para filtrar las ventas.
        end_date: Fecha de fin para filtrar las ventas.
    
    Returns:
        Optional[dict]: Detalles del producto si la consulta es exitosa, None en caso de error.
    """
    # Obtener la URL base de la API desde las variables de entorno
    api_url = EnvVariables.get_variable("RUNFOOD_PAYMENT_API_URL")
    
    # Construir la URL completa para el endpoint específico
    url = api_url.replace('__fecha_desde__', start_date).replace('__fecha_hasta__', end_date)
    
    # Configurar las cabeceras de autenticación
    headers = {
        "Content-Type": "application/json"
    }
    
    # Realizar la petición HTTP
    return make_http_request(url, method="GET", headers=headers)