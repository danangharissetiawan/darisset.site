from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse

from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

from six import python_2_unicode_compatible

from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from PIL import Image

from . import managers


class Profile(models.Model):
    # Relations
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", verbose_name=_(
        "user"), on_delete=models.CASCADE)
    # Attributes - Mandatory
    interaction = models.PositiveIntegerField(
        default=0, verbose_name=_("interaction"))
    images = models.ImageField(
        upload_to="blog/profile/thumbnail/%Y/%m/%d", blank=True, null=True, default="default.png")
    address = models.CharField(max_length=100, blank=True, null=True)
    profesi = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=250, blank=True, null=True)
    # Attributs - Optional
    # Object Manager
    objects = managers.ProfileManager()

    # Custom Properties
    @property
    def username(self):
        return self.user.username

    # Method
    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)

    #     img = Image.open(self.images.path)
    #     if img.height > 200 or img.width > 200:
    #         output_size = (200, 200)
    #         img.thumbnail(output_size)
    #         img.save(self.images.path)
    # # def get_absolute_url(self):
    #     return reverse("Profile_detail", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse("blog:penulis", kwargs={"user": self.user})

    # Meta & String
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("user",)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()


CATEGORY = (
    ("Jurnal", "jurnal"),
    ("Edukasi", "edukasi"),
    ("Entertaiment", "entertaiment"),
    ("News", "news"),
    ("Politics", "politics"),
    ("Teknologi", "teknologi")
)


class Post(models.Model):

    # Relations
    user = models.ForeignKey(Profile, related_name="post",
                             on_delete=models.CASCADE)
    tags = TaggableManager()
    # Attributes - Mandatory
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField()
    category = models.CharField(choices=CATEGORY, max_length=50)
    thumbnail = models.ImageField(
        upload_to="blog/post/thumbnail/%Y/%m/%d")
    body = RichTextUploadingField(config_name='default')
    publish = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    # Attributes - Optional
    bookmark = models.ManyToManyField(
        Profile, related_name="bookmarks", verbose_name=_("bookmark"), blank=True)
    active = models.BooleanField(default=False)

    # Object Manager
    objects = managers.PostManager()

    # Property
    

    # Method

    def save(self):
        self.slug = slugify(self.title)

        if self.active == True:
            self.publish = timezone.now()
        else:
            self.publish = None

        super().save()

    def bookmarks_hit(self):
        return self.bookmark.count()

    def _comments(self):
        return self.comments.count()

    # Meta & String

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ("-created",)

    def __str__(self):
        return "{}. {}".format(self.id, self.title)

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})


class Comment(models.Model):

    # Relations
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)

    # Attributes - Mandatory
    body = models.TextField()
    reply = models.ForeignKey("Comment", related_name="replies", verbose_name=_(
        "reply"), on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    # Attributes - Optional
    # Object Manager
    objects = managers.CommentManager()

    # Property
    # Method

    # Meta & String
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ("-created",)

    def __str__(self):
        return "{} --> {}".format(self.user, self.post)

    def get_absolute_url(self):
        return reverse("Comment_detail", kwargs={"pk": self.pk})
