import abc

class Email(abc.ABC):
    """
    Clase base para enviar correos electrónicos.
    """

    @abc.abstractmethod
    def send_email(self, subject: str, body: str, to: str) -> None:
        raise NotImplementedError
    
class SendAdapter(Email):
    """
    Implementación de la clase Email.
    """

    def send_email(self, subject: str, body: str, to: str) -> None:
        """
        Envía un correo electrónico.
        """
        pass