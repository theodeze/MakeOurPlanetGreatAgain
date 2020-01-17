from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


class User(AbstractUser):
    amount = models.PositiveIntegerField(_("Amount"), default=0)
    avatar = models.ImageField(_("Avatar"), upload_to="avatar", default="missing_user_avatar.png", height_field=None, width_field=None, max_length=None)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})
