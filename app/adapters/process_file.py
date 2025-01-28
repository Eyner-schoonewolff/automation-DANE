import openpyxl
import json
import abc
import csv
from typing import List, Dict, Any, Optional

# Definición de la clase base (ExcelProcessFile)
class ExcelProcessFile(abc.ABC):
    @abc.abstractmethod
    def read_data(self, file_path: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def extract_relevant_data(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def top_10_best_sellers(self) -> str:
        raise NotImplementedError
    
    @abc.abstractmethod
    def create_csv(self, top_10_data: List[Dict[str, Any]]) -> None:
        raise NotImplementedError


# Adaptador de la clase ExcelProcessFile
class AdapterExcel(ExcelProcessFile):

    def __init__(self) -> None:
        self.data: Optional[List[Dict[str, Any]]] = None
        self.top_10: Optional[List[Dict[str, Any]]] = None

    def read_data(self, file_path: str) -> None:
        """
        Lee los datos del archivo Excel y almacena los datos relevantes.
        """
        wb_obj = openpyxl.load_workbook(file_path)
        sheet_obj = wb_obj[wb_obj.sheetnames[2]]  # Seleccionar la tercera hoja

        # Crear una lista para almacenar los datos
        rows_data: List[Dict[str, Any]] = []

        # Recorrer las filas de la 9 a la 1354
        for row in range(9, 1354 + 1):
            producto = sheet_obj.cell(row=row, column=5).value
            marca = sheet_obj.cell(row=row, column=7).value
            cantidad = sheet_obj.cell(row=row, column=8).value
            precio = sheet_obj.cell(row=row, column=11).value

            if cantidad is not None:
                rows_data.append(
                    {
                        "producto": producto,
                        "marca": marca,
                        "cantidad": cantidad,
                        "precio": precio,
                    }
                )

        # Almacenar los datos en el atributo self.data
        self.data = rows_data

    def extract_relevant_data(self) -> None:
        """
        Extrae y organiza los 10 mejores productos con más cantidad vendida
        desde los datos previamente cargados.
        """
        if self.data is not None:
            # Ordenar los datos por 'cantidad' de mayor a menor
            sorted_data = sorted(self.data, key=lambda x: x["cantidad"], reverse=True)
            # Obtener los 10 primeros
            self.top_10 = sorted_data[:10]
        else:
            self.top_10 = None
            raise ValueError("No se ha cargado ninguna data previamente.")

    def top_10_best_sellers(self) -> str:
        """
        Función para obtener los 10 mejores productos y devolverlos en formato JSON y CSV.
        """
        self.extract_relevant_data()

        if self.top_10:
            # Convertir los resultados a JSON
            json_result = json.dumps(self.top_10, indent=4)

            # Crear archivo CSV
            self.create_csv(self.top_10)

            return json_result
        else:
            raise ValueError("No se pudieron obtener los mejores productos.")

    def create_csv(self, top_10_data: List[Dict[str, Any]]) -> None:
        """
        Crea un archivo CSV con los 10 productos más vendidos e incluye la sumatoria total.
        """
        if not top_10_data:
            raise ValueError("No hay datos para generar el archivo CSV.")
        
        csv_file = "top_10_best_sellers.csv"

        try:
            total_precio = sum(int(item['precio']) for item in top_10_data if isinstance(item, dict) and 'precio' in item)
            
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Escribir la cabecera
                writer.writerow(["Nombre del Producto", "Marca", "Cantidad"])

                for item in top_10_data:
                    if isinstance(item, dict) and 'producto' in item and 'marca' in item and 'cantidad' in item:
                        writer.writerow([item['producto'], item['marca'], item['cantidad']])
                    else:
                        raise ValueError(f"Error en los datos del producto: {item}")
                
                writer.writerow(["TOTAL", "", total_precio])
        
        except Exception as e:
            raise ValueError(f"Error al generar el archivo CSV: {e}")
