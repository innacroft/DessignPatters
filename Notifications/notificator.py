from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime


class NotificationFactory(ABC):
    """
    La clase NotificationFactory declara el método factory que devuelve
    un objeto de una clase Notification. Las subclases proporcionan
    la implementación específica para cada canal.
    """

    @abstractmethod
    def create_notification(self) -> Notification:
        """
        Método factory para crear notificaciones específicas
        """
        pass

    def send_notification(self, message: str, recipient: str) -> str:
        """
        Método principal que usa el factory method para crear y enviar
        notificaciones. Este método contiene la lógica de negocio común
        para todas las notificaciones.
        """
        # Crear la notificación usando el factory method
        notification = self.create_notification()
        
        # Preparar timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Enviar la notificación
        result = notification.send(message, recipient, timestamp)
        
        return result


"""
Implementaciones concretas del Factory para diferentes canales
"""


class EmailNotificationFactory(NotificationFactory):
    """
    Factory para crear notificaciones por email
    """
    
    def create_notification(self) -> Notification:
        return EmailNotification()


class SMSNotificationFactory(NotificationFactory):
    """
    Factory para crear notificaciones por SMS
    """
    
    def create_notification(self) -> Notification:
        return SMSNotification()


class SlackNotificationFactory(NotificationFactory):
    """
    Factory para crear notificaciones por Slack
    """
    
    def create_notification(self) -> Notification:
        return SlackNotification()


class PushNotificationFactory(NotificationFactory):
    """
    Factory para crear notificaciones push
    """
    
    def create_notification(self) -> Notification:
        return PushNotification()


class Notification(ABC):
    """
    Interface base para todas las notificaciones.
    Define el método que deben implementar todos los canales.
    """

    @abstractmethod
    def send(self, message: str, recipient: str, timestamp: str) -> str:
        """
        Método para enviar la notificación
        """
        pass


"""
Implementaciones concretas de notificaciones para cada canal
"""


class EmailNotification(Notification):
    def send(self, message: str, recipient: str, timestamp: str) -> str:
        return f"📧 EMAIL enviado a {recipient} [{timestamp}]\n" \
               f"   Asunto: Notificación importante\n" \
               f"   Mensaje: {message}\n" \
               f"   Estado: ✅ Entregado"


class SMSNotification(Notification):
    def send(self, message: str, recipient: str, timestamp: str) -> str:
        return f"📱 SMS enviado a {recipient} [{timestamp}]\n" \
               f"   Mensaje: {message}\n" \
               f"   Estado: ✅ Entregado"


class SlackNotification(Notification):
    def send(self, message: str, recipient: str, timestamp: str) -> str:
        return f"💬 SLACK enviado a #{recipient} [{timestamp}]\n" \
               f"   Mensaje: {message}\n" \
               f"   Estado: ✅ Entregado"


class PushNotification(Notification):
    def send(self, message: str, recipient: str, timestamp: str) -> str:
        return f"🔔 PUSH enviado a {recipient} [{timestamp}]\n" \
               f"   Título: Nueva notificación\n" \
               f"   Mensaje: {message}\n" \
               f"   Estado: ✅ Entregado"


class NotificationManager:
    """
    Clase para gestionar múltiples canales de notificación
    """
    
    def __init__(self):
        self.factories = {
            'email': EmailNotificationFactory(),
            'sms': SMSNotificationFactory(),
            'slack': SlackNotificationFactory(),
            'push': PushNotificationFactory()
        }
    
    def send_notification(self, channel: str, message: str,
                          recipient: str) -> str:
        """
        Envía una notificación por el canal especificado
        """
        if channel not in self.factories:
            available_channels = list(self.factories.keys())
            return f"❌ Error: Canal '{channel}' no soportado. " \
                   f"Canales disponibles: {available_channels}"
        
        factory = self.factories[channel]
        return factory.send_notification(message, recipient)
    
    def send_to_multiple_channels(self, channels: list, message: str,
                                  recipient: str) -> str:
        """
        Envía la misma notificación a múltiples canales
        """
        results = []
        for channel in channels:
            result = self.send_notification(channel, message, recipient)
            results.append(result)
        
        return "\n\n".join(results)


def demo_notifications():
    """
    Función de demostración para mostrar cómo usar el sistema de notificaciones
    """
    print("=== SISTEMA DE NOTIFICACIONES MULTICANAL ===\n")
    
    # Crear el gestor de notificaciones
    manager = NotificationManager()
    
    # Mensaje y destinatario de ejemplo
    message = "¡Tu pedido ha sido procesado exitosamente!"
    recipient = "usuario@ejemplo.com"
    
    print("📋 Enviando notificación individual por cada canal:\n")
    
    # Enviar por cada canal individualmente
    channels = ['email', 'sms', 'slack', 'push']
    for channel in channels:
        result = manager.send_notification(channel, message, recipient)
        print(f"{result}\n")
    
    print("\n" + "="*50 + "\n")
    print("📡 Enviando notificación a múltiples canales simultáneamente:\n")
    
    # Enviar a múltiples canales a la vez
    multi_result = manager.send_to_multiple_channels(
        ['email', 'sms', 'push'],
        "Recordatorio: Tu cita es mañana a las 3 PM",
        "cliente@empresa.com"
    )
    print(multi_result)


if __name__ == "__main__":
    demo_notifications()