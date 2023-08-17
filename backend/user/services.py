
from user.models import Subscription


class SubscribtionService:
    @classmethod
    def is_user_subscribed(cls, user, author):
        return Subscription.objects.filter(user=user, author=author).exists()

    @classmethod
    def subscribe(cls, user, author):
        Subscription.objects.get_or_create(user=user, author=author)

    @classmethod
    def unsubscribe(cls, user, author):
        Subscription.objects.filter(user=user, author=author).delete()
    