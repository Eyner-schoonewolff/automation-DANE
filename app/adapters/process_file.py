import openpyxl
import json
import abc
import csv


# Definición de la clase base (ExcelProcessFile)
class ExcelProcessFile(abc.ABC):
    @abc.abstractmethod
    def read_data(self, file_path: str) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def extract_relevant_data(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def top_10_best_sellers(self) -> None:
        raise NotImplementedError


# Adaptador de la clase ExcelProcessFile
class AdapterExcel(ExcelProcessFile):
    
    def __init__(self):
        self.data = None
    
    def read_data(self, file_path: str) -> None:
        """
        Lee los datos del archivo Excel y almacena los datos relevantes.
        """
        wb_obj = openpyxl.load_workbook(file_path)
        sheet_obj = wb_obj[wb_obj.sheetnames[2]]  # Seleccionar la tercera hoja
        
        # Crear una lista para almacenar los datos
        rows_data = []
        
        # Recorrer las filas de la 9 a la 1354
        for row in range(9, 1354 + 1):
            producto = sheet_obj.cell(row=row, column=5).value
            marca = sheet_obj.cell(row=row, column=7).value
            cantidad = sheet_obj.cell(row=row, column=8).value
            
            if cantidad is not None:
                rows_data.append({'producto': producto, 'marca': marca, 'cantidad': cantidad})
        
        # Almacenar los datos en el atributo self.data
        self.data = rows_data

    def extract_relevant_data(self) -> None:
        """
        Extrae y organiza los 10 mejores productos con más cantidad vendida
        desde los datos previamente cargados.
        """
        if self.data is not None:
            # Ordenar los datos por 'cantidad' de mayor a menor
            sorted_data = sorted(self.data, key=lambda x: x['cantidad'], reverse=True)
            # Obtener los 10 primeros
            self.top_10 = sorted_data[:10]
        else:
            print("No se ha cargado ninguna data previamente.")
            self.top_10 = None

    def top_10_best_sellers(self) -> None:
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
            return "No se pudieron obtener los mejores productos."

    def create_csv(self, top_10_data) -> None:
        """
        Crea un archivo CSV con los 10 productos más vendidos.
        """
        if not top_10_data:
            print("No hay datos para generar el archivo CSV.")
            return
        
        # Nombre del archivo CSV
        csv_file = "top_10_best_sellers.csv"

        try:
            # Escribir los datos en el archivo CSV
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Escribir la cabecera
                writer.writerow(["Nombre del Producto", "Marca", "Precio"])

                # Escribir las filas de datos
                for item in top_10_data:
                    if isinstance(item, dict) and 'producto' in item and 'marca' in item and 'cantidad' in item:
                        writer.writerow([item['producto'], item['marca'], item['cantidad']])
                    else:
                        print("Error en los datos del producto:", item)
            
            print(f"Archivo CSV '{csv_file}' generado con éxito.")
        except Exception as e:
            print(f"Error al generar el archivo CSV: {e}")
