from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url, include
# from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.flatpages import views
from django.contrib.sitemaps.views import sitemap

from .views import HomeView, home, home_files
from .apps.blog.views import contactView, successView
from .sitemaps import Post_Sitemap, Static_Sitemap, Profile_Sitemap, CategoryPostSitemap, TagsPostSitemap

sitemaps = {
    'post': Post_Sitemap(),
    'static': Static_Sitemap(),
    'profile': Profile_Sitemap(),
    'category': CategoryPostSitemap(),
    'tag': TagsPostSitemap(),
}

urlpatterns = [
    # path('<filename>', home_files, name='home-files'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^robots\.txt', include('robots.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),
]


urlpatterns += i18n_patterns(
    path('', HomeView.as_view(), name='home'),
    path('blog/', include('darisset.apps.blog.urls', namespace="blog")),
    path('admin/', admin.site.urls),
    path("contact/", contactView, name="contact"),
    path("contact-success/", successView, name="contact-success"),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    # path('us/', include('django.contrib.flatpages.urls')),
    path('about-us/', views.flatpage, {'url': '/en/about/'}, name='about'),
    path('privacy-policy/', views.flatpage, {'url': '/en/privacy-policy/'}, name='privacy-policy'),
    path('disclaimer/', views.flatpage, {'url': '/en/disclaimer/'}, name='disclaimer'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^newsletter/', include('newsletter.urls'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
# urlpatterns += 
