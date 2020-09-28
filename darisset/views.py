from django.shortcuts import render
from django.utils.timezone import now
from django.views.generic import ListView

from darisset.apps.blog.models import Post
from django.conf import settings

from seo.mixins.views import (
    ViewSeoMixin,
    ModelInstanceViewSeoMixin,
    UrlSeoMixin
)

import datetime


class HomeView(ViewSeoMixin, ListView):
    model = Post
    template_name = "darisset/index.html"
    context_object_name = "posts"
    ordering = "-created"
    paginate_by = 10
    seo_view = 'index'

    def get_queryset(self):
        self.queryset = self.model.objects.all().exclude(active=False)
        return super().get_queryset()

    def get_context_data(self, **kwargs):

        jurnals = self.model.objects.filter(category="Jurnal").exclude(
            active=False).order_by("-created")
        self.kwargs.update({"jurnals": jurnals})

        today = datetime.date.today()
        self.kwargs.update({'today': today, "now": now()})

        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        context['popular_posts'] = Post.objects.order_by('-hit_count_generic__hits')[:3]
        return context


def home(request):
    today = datetime.date.today()
    return render(request, 'darisset/index.html', {'today': today, 'now': now()})


def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")
