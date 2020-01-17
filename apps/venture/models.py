from django.db import models
from django.db.models import Model
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from datetime import date


class Venture(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    summary = models.CharField(_("Summary"), max_length=280)
    description = models.TextField(_("Description"))
    banner = models.ImageField(_("Banner"), upload_to="banner", default="missing_venture_banner.png", height_field=None,
                               width_field=None, max_length=None)
    creator = models.ForeignKey("authentication.User", verbose_name=_("Creator"), on_delete=models.CASCADE)

    created_at = models.DateTimeField(_("Created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True, auto_now_add=False)
    finished_at = models.DateField(_("Finished at"), auto_now=False, auto_now_add=False)

    #status = models.IntegerField(_("Status"))
    goal = models.PositiveIntegerField(_("Goal"))

    class Meta:
        verbose_name = _("Venture")
        verbose_name_plural = _("Ventures")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/ventures/%s' % self.id

    def comments(self):
        return Comment.objects.filter(what=self)

    def n_comments(self):
        return len(self.comments())

    def percent(self):
        return int((self.amount() / self.goal) * 100)

    def amount(self):
        return sum(f.amount for f in Pledge.objects.filter(to=self))

    def is_over(self):
        return self.remaining_days() < 0

    def contributors(self):
        return len(Pledge.objects.filter(to=self).values('who').distinct())

    def remaining_days(self):
        delta = self.finished_at - date.today()
        return delta.days


class Pledge(models.Model):
    amount = models.PositiveIntegerField(_("Amount"))
    who = models.ForeignKey("authentication.User", verbose_name=_("Who"), on_delete=models.CASCADE)
    to = models.ForeignKey(Venture, verbose_name=_("To"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Funding")
        verbose_name_plural = _("Fundings")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Funding_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    who = models.ForeignKey("authentication.User", verbose_name=_("Who"), on_delete=models.CASCADE)
    what = models.ForeignKey(Venture, verbose_name=_("What"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True, auto_now_add=False)
    message = models.TextField(_("Message"))

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Comment_detail", kwargs={"pk": self.pk})


class Follow(models.Model):
    follower = models.ForeignKey("authentication.User", verbose_name=_("Follower"), on_delete=models.CASCADE)
    following = models.ForeignKey(Venture, verbose_name=_("Following"), on_delete=models.CASCADE)
    subscribed = models.DateTimeField(_("Subscribed"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Follow")
        verbose_name_plural = _("Follows")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Follow_detail", kwargs={"pk": self.pk})


class Support(models.Model):
    who = models.ForeignKey("authentication.User", verbose_name=_("Who"), on_delete=models.CASCADE)
    to = models.ForeignKey(Venture, verbose_name=_("To"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Support")
        verbose_name_plural = _("Supports")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Support_detail", kwargs={"pk": self.pk})
