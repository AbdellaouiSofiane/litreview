from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

class UserFollows(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="+")
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="+")

    class Meta:
        unique_together = ('user', 'followed_user')
        verbose_name_plural = "User follows"

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"


# Add following field to User dynamically
user_model = get_user_model()
user_model.add_to_class('following', models.ManyToManyField('self',
    through=UserFollows, related_name='followers', symmetrical=False))