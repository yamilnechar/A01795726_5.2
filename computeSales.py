"""
Módulo para calcular el total de ventas a partir de archivos JSON.
Este script carga datos de productos y ventas, calcula el total
de ingresos y genera un archivo de resultados.
"""

import json
import time


def load_json(file_path):
    """Carga un archivo JSON y maneja errores."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no se encuentra.")
        return None
    except json.JSONDecodeError:
        print(f"Error: No se pudo decodificar el JSON {file_path}.")
        return None


def compute_total_sales(products, sales):
    """Calcula el total de ventas con base en el catálogo."""
    total_sales = 0
    errors = 0

    for sale in sales:
        if not isinstance(sale, dict):  # Verifica que la venta es un diccionario
            print("Advertencia: Venta con formato incorrecto, se omitirá.")
            errors += 1
            continue

        product_title = sale.get("Product")  # Cambia "product_id" por "Product"
        quantity = sale.get("Quantity", 0)  # Si no existe, usa 0

        if product_title is None:
            print("Advertencia: Venta sin 'Product', se omitirá.")
            errors += 1
            continue

        if product_title in products:
            total_sales += products[product_title] * quantity
        else:
            print(f"Advertencia: Producto '{product_title}' no encontrado en el catálogo.")
            errors += 1

    return total_sales, errors


# Define las rutas de los archivos en Google Drive
PRODUCTS_FILE = (
    "/content/drive/MyDrive/Colab Notebooks/MNA/TC4017 - Pruebas de Software/"
    "Semana 5/A5.2 Archivos de Apoyo/TC1/TC1.ProductList.json"
)
SALES_FILE = (
    "/content/drive/MyDrive/Colab Notebooks/MNA/TC4017 - Pruebas de Software/"
    "Semana 5/A5.2 Archivos de Apoyo/TC1/TC1.Sales.json"
)

start_time = time.time()

# Cargar datos desde JSON
products_data = load_json(PRODUCTS_FILE)
sales_data = load_json(SALES_FILE)

# Verificar estructura de los datos cargados
if products_data:
    print("Ejemplo de un producto:", products_data[0])  # Verifica la estructura
else:
    raise SystemExit(
        "Error: El archivo de productos está vacío o no tiene la estructura esperada."
    )

if sales_data:
    print("Ejemplo de una venta:", sales_data[0])  # Verifica la estructura
else:
    raise SystemExit(
        "Error: El archivo de ventas está vacío o no tiene la estructura esperada."
    )

# Convertir catálogo de productos a un diccionario de precios
try:
    product_prices = {
        p.get("title"): p.get("price", 0)
        for p in products_data if "title" in p and "price" in p
    }
except TypeError as exc:
    raise SystemExit("Error en el formato del archivo de productos.") from exc

# Validar que product_prices no está vacío
if not product_prices:
    raise SystemExit("Error: No se pudo generar el catálogo de precios correctamente.")

# Calcular el total de ventas
total, error_count = compute_total_sales(product_prices, sales_data)

# Generar el texto de salida
result_text = (
    f"Total de ventas: ${total:.2f}\n"
    f"Errores encontrados: {error_count}\n"
    f"Tiempo de ejecución: {time.time() - start_time:.4f} segundos\n"
)

# Mostrar resultado en pantalla
print(result_text)

# Guardar los resultados en un archivo
with open("SalesResults.txt", "w", encoding="utf-8") as output_file:
    output_file.write(result_text)
