from app.adapters import localization_web_process


class ServiceAutomatication:
    def __init__(self, repo: localization_web_process.DANEAdapter) -> None:
        self.repo: localization_web_process.DANEAdapter = repo

    def process_generate_excel(
        self,
        url: str,
    ) -> str:
        driver = None
        try:
            driver = self.repo.open_url(url)
            self.repo.locate_section(driver)
            self.repo.download_file(driver)
            self.repo.generate_screenshot(driver, "screenshot.png")
        except Exception as e:
            print(f"An error occurred: {e}")
            # Aquí podrías agregar más manejo de errores, como logging
        finally:
            if driver:
                driver.quit()
