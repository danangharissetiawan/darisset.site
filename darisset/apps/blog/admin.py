from django.contrib import admin
from django.utils import timezone
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin

from seo.admin import ModelInstanceSeoInline


from . import models


admin.site.site_header = 'Darisset Dashboard'

admin.site.unregister(FlatPage)
# @admin.register(FlatPage)
class FlatPageAdmin(FlatPageAdmin):
    inlines = [ModelInstanceSeoInline]

admin.site.register(FlatPage, FlatPageAdmin)

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "interaction",)
    search_fields = ["user__username"]


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    change_form_template = "darisset/admin/blog/base_site_blog.html"
    list_display = ("title", "user",
                    "bookmarks_hit", "_comments", "created", "publish", "active")
    search_fields = ["title", "category"]
    list_filter = ["active", "category", "created"]
    readonly_fields = ("slug", "created", "modified", "active", "publish")
    fieldsets = (
        (None, {
            "fields": (
                "user", "title", "thumbnail", "category", "tags", "body",
            ),
        }),
        ("Advance Options | cannot be changed", {
            'classes': ('collapse',),
            "fields": (
                "slug", "active", "created", "modified", "publish"
            )
        })
    )
    save_on_top = True
    actions = ["published", "delete_status_publish"]
    inlines = [ModelInstanceSeoInline]

    def published(self, request, queryset):
        queryset.update(active=True, publish=timezone.now())

    def delete_status_publish(self, request, queryset):
        queryset.update(active=False, publish=None)



@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "body", "active", "created")
    search_fields = ["body"]
    readonly_fields = ("active", "created", "reply")
    fieldsets = (
        (None, {
            "fields": (
                "user", "post", "body"
            ),
        }),
        ("Advance Options | cannot be changed", {
            'classes': ('collapse',),
            "fields": (
                "active", "created", "reply"
            )
        })
    )

    actions = ["activate"]

    def has_add_permission(self, request):
        return False

    def activate(self, request, queryset):
        queryset.update(active=True)
