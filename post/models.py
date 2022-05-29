from django.conf import settings
from django.utils.text import slugify
from django.db import models


def ticket_picture_path(instance, filename):
    slug = slugify(instance.title)
    extension = filename.split('.')[-1]
    return 'ticket_pictures/{0}.{1}'.format(slug, extension)


class Ticket(models.Model):
    title = models.CharField('title', max_length=250)
    description = models.TextField(
        'description', max_length=1000, blank=True, null=True)
    picture = models.ImageField(
        'Image', upload_to=ticket_picture_path, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets")

    def __str__(self):
        return f'ticket n°{self.id} of {self.user.username}'
