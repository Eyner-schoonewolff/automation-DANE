from app.adapters import localization_web_process, process_file, calculate_file, email


class ServiceAutomation:
    """
    Clase para coordinar procesos de descarga y análisis.
    """

    def __init__(
        self,
        scraping: localization_web_process.DANEAdapter,
        processor: process_file.ExcelAdapter,
        calculation: calculate_file.ExcelCalculationAdapter,
        email: email.SendAdapter,
    ):
        self.scraping = scraping
        self.processor = processor
        self.calculation = calculation
        self.email = email

    def process_generate_excel(self, url: str) -> str:
        """
        Realiza la descarga de un archivo Excel desde una URL.
        """
        driver = self.scraping.open_url(url)
        try:
            self.scraping.locate_section(driver)
            file_path = self.scraping.download_file(driver)
            self.scraping.generate_screenshot(driver, "downloads/screenshot.png")
        finally:
            driver.quit()
        return file_path

    def process_excel(self, file_path: str) -> dict:
        """
        Procesa un archivo Excel y luego calcular reporte.
        """
        # Leer los datos del archivo Excel
        all_data_file = self.processor.read_data(file_path)

        # Extraer los 10 productos más vendidos
        top_10_products = self.processor.extract_relevant_data()

        path_csv = self.processor.generate_csv()
        # Calcular el total de productos
        products = self.calculation.calculate_products(all_data_file)
        
        # Calcular el total de los productos más vendidos (Top 10)
        top_10_total = self.calculation.calculate_total_top_10(top_10_products)

        # Calcular el porcentaje de ventas de los 10 productos más vendidos
        percentage = self.calculation.calculate_percentage(products, top_10_total)

        # Devolver los resultados en un diccionario
        return {
            "TOTAL_PRODUCTS": products,
            "TOP_10_TOTAL": top_10_total,
            "PERCENTAGE": percentage,
            "PATH_CSV": path_csv,
        }

    def process_email(self, data: dict, email: str) -> None:
        try:
            template = self.email.read_html_template("templates", "body")
            self.email.add_file_email(data["PATH_CSV"])
            self.email.send_email(template, data, email)
        except Exception as e:
            print(f"An error occurred while processing the email: {e}")
