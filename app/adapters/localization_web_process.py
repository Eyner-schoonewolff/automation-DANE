import abc
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

class LocalizationWebProcess(abc.ABC):
    @abc.abstractmethod
    def open_url(self, url: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def locate_section(self, driver) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def download_file(self, driver) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def generate_screenshot(self, driver, file_path: str) -> None:
        raise NotImplementedError


class DANEAdapter(LocalizationWebProcess):
    
    def __init__(self):
        # Configurar las opciones para Chrome
        self.options = Options()
        self.options.headless = True  

    def open_url(self, url: str) -> str:
        driver = webdriver.Chrome(options=self.options)  
        driver.get(url)
        return driver

    def locate_section(self, driver) -> None:
        time.sleep(5)  # Esperar a que la página cargue completamente
        section = driver.find_element(By.XPATH, "//h2[contains(text(), 'Precios de los productos de primera necesidad para los colombianos en tiempos del COVID-19')]")
        driver.execute_script("arguments[0].scrollIntoView();", section)

    def download_file(self, driver) -> None:
        # Localiza el enlace al archivo basado en su clase
        link = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-gray")
        file_url = link.get_attribute('href')  # Obtiene el atributo href del enlace

        # Validar si la URL ya incluye el esquema completo
        if not file_url.startswith("http"):
            file_url = f"https://www.dane.gov.co{file_url}" 

        # Descarga el archivo usando requests
        response = requests.get(file_url)

        # Manejo de errores en la descarga
        if response.status_code != 200:
            raise Exception(f"Error al descargar el archivo: {response.status_code}")

        # Guarda el archivo descargado
        file_path = os.path.join(os.getcwd(), 'anexo_referencias_mas_vendidas.xlsx')
        with open(file_path, 'wb') as file:
            file.write(response.content)


    def generate_screenshot(self, driver, file_path: str) -> None:
        
        if not file_path.endswith(".png"):
            file_path += ".png"
        
        driver.save_screenshot(file_path)


