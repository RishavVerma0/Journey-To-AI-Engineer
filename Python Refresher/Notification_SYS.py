class Notification:
    def send(self, message):
        raise NotImplementedError("Subclass must implement send()")


class EmailNotification(Notification):
    def send(self, message):
        print(f"Email sent: {message}")


class SMSNotification(Notification):
    def send(self, message):
        print(f"SMS sent: {message}")


class PushNotification(Notification):
    def send(self, message):
        print(f"Push notification sent: {message}")


class NotificationManager:
    def __init__(self, notification):
        self.notification = notification

    def notify(self, message):
        self.notification.send(message)


notifications = [
    EmailNotification(),
    SMSNotification(),
    PushNotification()
]

for notification in notifications:
    manager = NotificationManager(notification)
    manager.notify("Your order has been shipped!")