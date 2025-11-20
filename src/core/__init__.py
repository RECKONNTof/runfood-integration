"""
Módulo core con funcionalidades básicas.

Provee utilidades para peticiones HTTP y gestión de variables de entorno.
"""

from .make_http_request import make_http_request
from .get_env_variables import EnvVariables

__all__ = [make_http_request, EnvVariables]