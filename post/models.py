from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


def ticket_picture_path(instance, filename):
    slug = slugify(instance.title)
    extension = filename.split('.')[-1]
    return 'ticket_pictures/{0}.{1}'.format(slug, extension)


class Post(models.Model):
    title = models.CharField(
        'titre', max_length=250)
    description = models.TextField(
        'description', max_length=1000, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='utilisateur')
    time_created = models.DateTimeField(
        'date de création', auto_now_add=True)

    class Meta:
        abstract = True


class Ticket(Post):
    picture = models.ImageField(
        'Image', upload_to=ticket_picture_path, blank=True, null=True)

    def __str__(self):
        return f'ticket n°{self.id} of {self.user.username}'


# class Review(models.Model):
#     ticket = models.ForeignKey(
#         Ticket, on_delete=models.CASCADE, related_name="reviews")
#     rating = models.PositiveSmallIntegerField(
#         'note', validators=[MinValueValidator(0), MaxValueValidator(5)])
