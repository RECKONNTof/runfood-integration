"""
Módulo para gestión de variables de entorno.

Provee funcionalidad para cargar y validar variables de entorno requeridas
por la aplicación desde archivos .env.
"""

import os
from typing import Literal
from dotenv import load_dotenv


class EnvVariables:
    # Definir el tipo para las claves de variables de entorno permitidas
    ENV_VARIABLE_KEY = Literal[
        "TOKEN",
        "RUNFOOD_PRODUCT_API_URL",
        "RUNFOOD_PAYMENT_API_URL",
        "RECKONNT_SALE_API_URL"
    ]
    
    env_keys: list[str] = [
        "TOKEN",
        "RUNFOOD_PRODUCT_API_URL",
        "RUNFOOD_PAYMENT_API_URL",
        "RECKONNT_SALE_API_URL"
    ]
    env_variables: dict[str, str] | None = None
    
    @staticmethod
    def load_env_variables() -> dict[str, str]:
        """
        Carga las variables de entorno desde el archivo .env y valida que estén definidas.
        
        Returns:
            dict[str, str]: Diccionario con las variables de entorno cargadas.
            
        Raises:
            EnvironmentError: Si alguna variable de entorno requerida no está definida.
        """
        load_dotenv()
        env_vars: dict[str, str] = {}
        
        # Si ya fueron cargadas previamente, retornar las existentes
        if EnvVariables.env_variables is not None:
            return EnvVariables.env_variables
        
        # Validar que todas las variables de entorno necesarias estén definidas
        for key in EnvVariables.env_keys:
            env_value = os.getenv(key)
            if env_value is None:
                raise EnvironmentError(f"Variable de entorno {key} no está definida.")
            env_vars[key] = env_value
        
        # Guardar en cache las variables cargadas
        EnvVariables.env_variables = env_vars
        return env_vars
    
    @staticmethod
    def get_variable(key: ENV_VARIABLE_KEY) -> str:
        """
        Obtiene el valor de una variable de entorno específica.
        
        Args:
            key: La clave de la variable de entorno a obtener.
            
        Returns:
            str: El valor de la variable de entorno.
            
        Raises:
            RuntimeError: Si las variables de entorno no han sido cargadas.
            KeyError: Si la clave no existe en las variables cargadas.
        """
        if EnvVariables.env_variables is None:
            raise RuntimeError(
                "Las variables de entorno no han sido cargadas. "
                "Llame a load_env_variables() primero."
            )
        return EnvVariables.env_variables[key]
    