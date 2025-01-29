import abc
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os
from fastapi import HTTPException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

smtp_user = os.environ.get("SMTP_USER")
smtp_password = os.environ.get("SMTP_PASSWORD")
smtp_server = os.environ.get("SMTP_SERVER")
smtp_port = os.environ.get("SMTP_PORT")


class Email(abc.ABC):
    """
    Clase base para enviar correos electrónicos.
    """

    @abc.abstractmethod
    def read_html_template(self, folder, file):
        raise NotImplementedError

    @abc.abstractmethod
    def send_email(self, template, data: dict, email: str | list) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_file_email(self, attachment_path: str) -> None:
        raise NotImplementedError


class SendAdapter(Email):
    """
    Send Email Adapter
    """
    def __init__(self):
        self.email_obj = MIMEMultipart()

    def read_html_template(self, folder, file):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "..", folder, f"{file}.html")
        file_path = os.path.abspath(file_path)
        print(file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                template = file.read()
            logger.debug(f"Template {folder}/{file} leído correctamente.")
        except FileNotFoundError:
            logger.error(f"No se encontró el template {folder}/{file}")
            raise HTTPException(
                status_code=404, detail=f"No se encontró el template {folder}/{file}"
            )
        except Exception as e:
            logger.error(f"Error al leer el template: {e}")
            raise HTTPException(status_code=500, detail=f"Error al leer el template: {e}")

        return template

    def send_email(self, template: str, data: dict, email: str | list) -> None:
        try:
            # Replace template values
            for key, value in data.items():
                template = template.replace(f"%{key.upper()}%", str(value))

            # Create email
            self.email_obj["From"] = "psciologiacontacto@gmail.com"
            self.email_obj["Subject"] = "Reporte de precios de productos de primera necesidad"

            # Handle email_to single or multiple emails
            if isinstance(email, str):
                self.email_obj["To"] = email
                recipient_list = [email]
            elif isinstance(email, list):
                self.email_obj["To"] = ", ".join(email)
                recipient_list = email

            # Attach the email body (HTML content)
            email_body = MIMEText(template, "html")
            self.email_obj.attach(email_body)

            # Send email
            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()  # Esto es importante para Gmail, habilitar TLS
                    server.login(smtp_user, smtp_password)  # Aquí usamos el usuario y contraseña de Gmail
                    server.sendmail(self.email_obj["From"], recipient_list, self.email_obj.as_string())
                    logger.debug("Correo enviado correctamente.")
                    return {"message": "Correo enviado correctamente"}
            except smtplib.SMTPException as e:
                logger.error(f"Error al enviar el correo: {e}")
                return {"message": f"Error al enviar el correo: {e}"}
            except Exception as e:
                logger.error(f"Error inesperado al enviar el correo: {e}")
                return {"message": f"Error inesperado al enviar el correo: {e}"}

        except Exception as e:
            logger.error(f"Error en send_email: {e}")
            return {"message": f"Error en send_email: {e}"}

    def add_file_email(self, attachment_path: str) -> None:
        """
        Adjunta un archivo al correo electrónico.
        """
        try:
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())

                encoders.encode_base64(part)

                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(attachment_path)}",
                )

                self.email_obj.attach(part)
                logger.debug(f"Archivo adjunto {attachment_path} agregado correctamente.")
            else:
                raise ValueError("El archivo adjunto no existe o la ruta es inválida.")
        except FileNotFoundError:
            logger.error(f"El archivo no fue encontrado en la ruta: {attachment_path}")
        except ValueError as e:
            logger.error(f"Error en la ruta del archivo adjunto: {e}")
        except Exception as e:
            logger.error(f"Error al adjuntar el archivo: {e}")
