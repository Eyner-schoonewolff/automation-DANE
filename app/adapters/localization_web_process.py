import abc
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

class LocalizationWebProcess(abc.ABC):
    """
    Clase base para procesos de localización web.
    """

    @abc.abstractmethod
    def open_url(self, url: str):
        raise NotImplementedError

    @abc.abstractmethod
    def locate_section(self, driver) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def download_file(self, driver) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def generate_screenshot(self, driver, file_path: str) -> None:
        raise NotImplementedError


class DANEAdapter(LocalizationWebProcess):
    """
    Implementación de la clase LocalizationWebProcess.
    """

    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")

    def open_url(self, url: str):
        driver = webdriver.Chrome(options=self.options)
        driver.get(url)
        return driver

    def locate_section(self, driver) -> None:
        time.sleep(5)
        section = driver.find_element(
            By.XPATH,
            "//h2[contains(text(), 'Precios de los productos de primera necesidad')]",
        )
        driver.execute_script("arguments[0].scrollIntoView();", section)

    def download_file(self, driver) -> str:
        link = driver.find_element(
            By.CSS_SELECTOR, "a.btn.btn-gray[title='Anexo referencias mas vendidas']"
        )
        file_url = link.get_attribute("href")
        response = requests.get(file_url)
        if response.status_code != 200:
            raise Exception(f"Error al descargar archivo: {response.status_code}")

        file_path = os.path.join(os.getcwd(), "downloads/anexo_referencias_mas_vendidas.xlsx")
        with open(file_path, "wb") as file:
            file.write(response.content)
        return file_path

    def generate_screenshot(self, driver, file_path: str) -> None:
        driver.save_screenshot(file_path if file_path.endswith(".png") else f"{file_path}.png")
