"""
Módulo para realizar peticiones HTTP.

Provee funcionalidad genérica para hacer solicitudes HTTP con diferentes métodos.
"""

import requests
from typing import Literal, Optional

# Tipo literal para los métodos HTTP soportados
HttpMethod = Literal["GET", "POST", "PUT", "DELETE"]


def make_http_request(
    url: str, 
    method: HttpMethod = "GET", 
    data: Optional[dict] = None, 
    headers: Optional[dict] = None
) -> Optional[dict]:
    """
    Realiza una petición HTTP al endpoint especificado.
    
    Args:
        url: La URL del endpoint a consultar.
        method: El método HTTP a utilizar (GET, POST, PUT, DELETE).
        data: Datos a enviar en el cuerpo de la petición (para POST/PUT).
        headers: Cabeceras HTTP personalizadas para la petición.
    
    Returns:
        Optional[dict]: Respuesta JSON parseada si es exitosa, None en caso de error.
    
    Raises:
        ValueError: Si se especifica un método HTTP no soportado.
    """
    try:
        # Ejecutar la petición según el método especificado
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Método HTTP no soportado: {method}")

        # Verificar que la respuesta sea exitosa (códigos 2xx)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")
        try:
            error_content = response.json()
            print(f"Respuesta del servidor: {error_content}")
        except ValueError:
            print(f"Respuesta del servidor (texto): {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la petición HTTP: {e}")
        return None