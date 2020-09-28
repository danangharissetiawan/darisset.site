from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.contrib.flatpages.models import FlatPage

from taggit.models import Tag

from darisset.apps.blog.models import Post, Profile

class Static_Sitemap(Sitemap):

    priority = 1.0
    changefreq = 'daily'


    def items(self):
        return FlatPage.objects.all()


class TagsPostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Tag.objects.all().order_by('name')

    def location(self, item):
        return reverse('blog:tag', kwargs={'tag': item.name})    


class CategoryPostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    # protocol = ("http" or "https")

    def items(self):
        return Post.objects.all().order_by('category')
    
    def location(self, item):
        return reverse('blog:category', kwargs={'category': item.category})

class Post_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    protocol = ("http" or "https")

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj): 
        return obj.modified

class Profile_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Profile.objects.all()

