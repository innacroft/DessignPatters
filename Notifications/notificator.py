import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotificationChannel(Enum):
    """
    Enumeration of available notification channels.
    Facilitates extension and avoids string type errors.
    """
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    SLACK = "slack"
    TELEGRAM = "telegram"


class NotificationMessage:
    """
    Class that encapsulates all notification information.
    Allows reusing the same message across multiple channels.
    """

    def __init__(self, recipient: str, subject: str, content: str,
                 channels: List[NotificationChannel],
                 metadata: Dict[str, Any] = None):
        self.recipient = recipient
        self.subject = subject
        self.content = content
        self.channels = channels
        self.metadata = metadata or {}
    
    def __str__(self):
        return (f"NotificationMessage(recipient='{self.recipient}', "
                f"subject='{self.subject}')")


class ChannelNotifier(ABC):

    @abstractmethod
    def send(self, message: NotificationMessage) -> bool:
        pass

    @abstractmethod
    def get_channel(self) -> NotificationChannel:
        pass


class EmailNotifier(ChannelNotifier):
    def send(self, message: NotificationMessage) -> bool:
        try:
            logger.info("📧 Sending email")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    def get_channel(self) -> NotificationChannel:
        return NotificationChannel.EMAIL


class SMSNotifier(ChannelNotifier):
    def send(self, message: NotificationMessage) -> bool:
        try:
            logger.info("Sending SMS")
            return True
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            return False
    
    def get_channel(self) -> NotificationChannel:
        return NotificationChannel.SMS


class WhatsAppNotifier(ChannelNotifier):
    def send(self, message: NotificationMessage) -> bool:
        try:
            logger.info(f"Sending WhatsApp")
            return True
        except Exception as e:
            logger.error(f"Error sending WhatsApp: {e}")
            return False

    def get_channel(self) -> NotificationChannel:
        return NotificationChannel.WHATSAPP


class SlackNotifier(ChannelNotifier):   
    def send(self, message: NotificationMessage) -> bool:
        try:
            logger.info(f"Sending Slack")
            return True
        except Exception as e:
            logger.error(f"Error sending Slack: {e}")
            return False

    def get_channel(self) -> NotificationChannel:
        return NotificationChannel.SLACK


class TelegramNotifier(ChannelNotifier):
    def send(self, message: NotificationMessage) -> bool:
        try:
            logger.info(f"Sending Telegram")
            return True
        except Exception as e:
            logger.error(f"Error sending Telegram: {e}")
            return False

    def get_channel(self) -> NotificationChannel:
        return NotificationChannel.TELEGRAM


class NotifierRegistry:
    """
    Dynamic registry of notifiers.
    Allows adding/removing channels at runtime.
    """
    def __init__(self):
        self.notifiers: Dict[NotificationChannel, ChannelNotifier] = {}
        self._register_default_channels()

    def _register_default_channels(self):
        self.register_channel(EmailNotifier())
        self.register_channel(SMSNotifier())
        self.register_channel(WhatsAppNotifier())
        self.register_channel(SlackNotifier())
        self.register_channel(TelegramNotifier())

    def register_channel(self, notifier: ChannelNotifier):
        channel = notifier.get_channel()
        self.notifiers[channel] = notifier
        logger.info(f"Channel registered: {channel.value}")

    def remove_channel(self, channel: NotificationChannel):
        if channel in self.notifiers:
            del self.notifiers[channel]
            logger.info(f"Channel removed: {channel.value}")
        else:
            logger.warning(f"Channel not found: {channel.value}")

    def get_notifier(self, channel: NotificationChannel) -> ChannelNotifier:
        """Gets the notifier for a specific channel."""
        return self.notifiers.get(channel)

    def get_available_channels(self) -> List[NotificationChannel]:
        """Returns the list of available channels."""
        return list(self.notifiers.keys())


class NotificationService:
    """
    Main service for sending notifications.
    Coordinates sending to multiple channels without duplicating logic.
    """

    def __init__(self):
        self.registry = NotifierRegistry()

    def send_notification(self, message: NotificationMessage) -> Dict[str, bool]:
        logger.info(f"🚀 Starting notification sending to {message.recipient}")
        results = {}
        for channel in message.channels:
            notifier = self.registry.get_notifier(channel)
            if notifier:
                try:
                    result = notifier.send(message)
                    results[channel.value] = result
                    status = "Success" if result else "Failed"
                    logger.info(f"   {channel.value}: {status}")
                except Exception as e:
                    logger.error(f"   {channel.value}: Error - {e}")
                    results[channel.value] = False
            else:
                logger.warning(f"   {channel.value}:  Channel not available")
                results[channel.value] = False
        successful = sum(1 for r in results.values() if r)
        total = len(results)
        logger.info(f"Summary: {successful}/{total} successful")

        return results

    def register_new_channel(self, notifier: ChannelNotifier):
        self.registry.register_channel(notifier)

    def remove_channel(self, channel: NotificationChannel):
        self.registry.remove_channel(channel)

    def get_available_channels(self) -> List[NotificationChannel]:
        return self.registry.get_available_channels()



class PushNotifier(ChannelNotifier):
    def send(self, message: NotificationMessage) -> bool:
        try:
            logger.info(f"Sending Push to {message.recipient}: {message.content}")
            return True
        except Exception as e:
            logger.error(f"Error sending Push: {e}")
            return False

    def get_channel(self) -> NotificationChannel:
        return NotificationChannel.TELEGRAM


def demo_notification_system():
    service = NotificationService()
    message = NotificationMessage(
        recipient="customer@company.com",
        subject="Order Confirmed",
        content="Your order #12345 has been processed successfully.",
        channels=[
            NotificationChannel.EMAIL, NotificationChannel.SMS,
            NotificationChannel.WHATSAPP],
        metadata={"order_id": "12345", "priority": "high"}
    )

    # Send notification
    print(f"\nSending notification to: {message.recipient}")
    print(f"Using channels: {[c.value for c in message.channels]}")
    print("-" * 50)
    results = service.send_notification(message)

    print(f"\nDemo completed successfully! {results}")
    print("=" * 50)


if __name__ == "__main__":
    demo_notification_system()
