"""
Punto de entrada principal de la aplicación.

Inicializa la aplicación cargando las variables de entorno necesarias
y configurando el entorno de ejecución.
"""

import datetime
from .core.get_env_variables import EnvVariables
from .controllers.sales_integration_controller import (
    get_and_process_sales,
    send_sales_to_server
)


def main():
    """
    Función principal que inicializa la aplicación.
    
    Carga las variables de entorno requeridas, obtiene las ventas del día anterior,
    las procesa y las envía al servidor Reckonnt.
    """
    try:
        # Cargar y validar las variables de entorno
        EnvVariables.load_env_variables()
        print("✓ Variables de entorno cargadas correctamente")
        
        # Obtener las fechas para consultar las ventas
        current_date = datetime.datetime.now()
        start_date = (current_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        end_date = current_date.strftime("%Y-%m-%d")
        
        print(f"\nConsultando ventas desde {start_date} hasta {end_date}")
        
        # Obtener y procesar las ventas
        sales_data = get_and_process_sales(start_date, end_date)
        
        if sales_data:
            # Enviar los datos al servidor
            result = send_sales_to_server(start_date, end_date, sales_data)
            
            if result:
                print("\n✓ Proceso completado exitosamente")
            else:
                print("\n✗ No se pudo enviar los datos al servidor")
        else:
            print("\n✗ No se pudieron obtener los datos de ventas")
            
    except EnvironmentError as e:
        print(f"\n✗ Error al cargar las variables de entorno: {e}")
        print("Asegúrate de crear un archivo .env con las variables necesarias")
        raise
    except Exception as e:
        print(f"\n✗ Se produjo un error: {e}")
        raise
