from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class ItemList(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    PRIORITY_CHOICES = [
        ('doFirst', 'Do First'),
        ('schedule', 'Schedule'),
        ('delegate', 'Delegate'),
        ('eliminate', 'Eliminate')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=50, null=True, blank=True, choices=PRIORITY_CHOICES)
    position_x = models.FloatField(null=True, blank=True)
    position_y = models.FloatField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_list = models.ForeignKey('ItemList', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)  # Store completion status
    in_matrix = models.BooleanField(default=True)  # Store in_matrix status

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_lists_created = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()