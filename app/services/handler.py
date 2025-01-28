from app.adapters import localization_web_process, process_file


class ServiceAutomatication:
    def __init__(
        self,
        repo: localization_web_process.DANEAdapter,
        processor: process_file.AdapterExcel,
    ) -> None:
        self.repo: localization_web_process.DANEAdapter = repo
        self.processor: process_file.AdapterExcel = processor

    def process_generate_excel(
        self,
        url: str,
    ) -> str:
        driver = None
        try:
            driver = self.repo.open_url(url)
            self.repo.locate_section(driver)
            file_path = self.repo.download_file(driver)
            self.repo.generate_screenshot(driver, "screenshot.png")
        except Exception as e:
            print(f"An error occurred: {e}")
            # Aquí podrías agregar más manejo de errores, como logging
        finally:
            if driver:
                driver.quit()
        
        return file_path

    def process_excel(self, file_path: str) -> None:
        self.processor.read_data(file_path)
        top_10 = self.processor.top_10_best_sellers()
        print(top_10)
     
        
