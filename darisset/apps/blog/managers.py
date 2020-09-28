from django.db import models


class ProfileManager(models.Manager):
    pass
    # def get_queryset(self):
    #     return super().get_queryset().filter()


class TagsManager(models.Manager):
    pass


class PostManager(models.Manager):
    pass


class CommentManager(models.Manager):
    pass
