from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from articles.models import Articles
from django.utils import timezone
from django.db.models.signals import pre_save



"""
check_status값이 True값으로 전환될때 해당 시간을 저장함
"""
@receiver(pre_save, sender=Articles)
def update_complete_at(sender, instance, **kwargs):
            if instance.check_status:
                instance.complete_at = timezone.now()