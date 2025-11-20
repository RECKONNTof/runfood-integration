"""
Módulo para procesar y limpiar datos de ventas.

Provee funcionalidad para eliminar campos innecesarios y procesar
listas de elementos de ventas.
"""

from typing import List, Dict, Any


def remove_unwanted_fields(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Elimina campos innecesarios de un elemento de venta.
    
    Args:
        item: Diccionario con los datos del elemento de venta.
    
    Returns:
        Dict[str, Any]: Elemento procesado sin los campos innecesarios.
    """
    fields_to_remove = [
        "id", "id_md", "idLinea", "linea", "Categoria", "Familia", 
        "ivaLinea", "telefono", "direccion", "Estado", "baseIva", 
        "base0", "iva"
    ]
    
    # Crear una copia del item para no modificar el original
    processed_item = item.copy()
    
    # Eliminar los campos especificados si existen
    for field in fields_to_remove:
        processed_item.pop(field, None)
    
    return processed_item


def process_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Procesa una lista de elementos eliminando campos innecesarios de cada uno.
    
    Args:
        items: Lista de elementos a procesar.
    
    Returns:
        List[Dict[str, Any]]: Lista de elementos procesados.
    """
    if not items:
        return []
    
    processed_items = []
    for item in items:
        processed_item = remove_unwanted_fields(item)
        processed_items.append(processed_item)
    
    return processed_items
