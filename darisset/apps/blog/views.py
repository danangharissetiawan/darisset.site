import urllib
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, View, ListView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

from hitcount.views import HitCountDetailView
from hitcount.models import Hit, HitCount

from seo.mixins.views import (
    ViewSeoMixin,
    ModelInstanceViewSeoMixin,
    UrlSeoMixin
)

from darisset.apps import blog
from functools import wraps
from .forms import CommentForm, ContactForm
from .models import Post, Comment, Profile



def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                subject = form.cleaned_data['subject']
                from_email = form.cleaned_data['from_email']
                message = form.cleaned_data['message']
                try:
                    send_mail(subject, message, from_email, ['administrator@darisset.site'])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, "Success! Thank you for your message.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

    return render(request, "darisset/blog/contact.html", {'form': form, 'title': 'Contact'})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')


class BookmarkView(ViewSeoMixin, LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "posts"
    template_name = "darisset/blog/bookmarks.html"
    paginate_by = 8
    seo_view = 'index'

    def get_queryset(self):
        users = self.request.user.profile
        self.queryset = users.bookmarks.all()
        return super().get_queryset()


class PopularView(ViewSeoMixin, ListView):
    model = Post
    template_name = "darisset/blog/categories.html"
    context_object_name = "posts"
    ordering = "-created"
    paginate_by = 8
    seo_view = 'index'

    def get_queryset(self):
        self.queryset = Post.objects.order_by('-hit_count_generic__hits')
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Popular Post"
        return context


class CategoryView(ViewSeoMixin, ListView):
    model = Post
    template_name = "darisset/blog/categories.html"
    context_object_name = 'posts'
    ordering = '-created'
    paginate_by = 8
    seo_view = 'index'

    def get_queryset(self):
        categories = self.model.objects.filter(
            category=self.kwargs["category"]).exclude(active=False)
        self.queryset = categories
        return super().get_queryset()

    def get_context_data(self, **kwargs):

        self.kwargs.update({
        'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        })

        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context["title"] = self.kwargs["category"]
        return context


class TagView(ViewSeoMixin, ListView):
    model = Post
    template_name = "darisset/blog/categories.html"
    context_object_name = "posts"
    ordering = "-created"
    paginate_by = 5
    seo_view = 'index'

    def get_queryset(self):
        self.queryset = self.model.objects.filter(
            tags__name__contains=self.kwargs['tag'])
        print(self.queryset)
        return super().get_queryset()

    def get_context_data(self, **kwargs):

        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context["title"] = self.kwargs["tag"]

        context['popular_posts'] = Post.objects.order_by('-hit_count_generic__hits')[:3]
        return context


class PenulisView(ViewSeoMixin, ListView):
    model = Post
    template_name = "darisset/blog/penulis.html"
    context_object_name = "posts"
    soe_view = 'index'

    def get_queryset(self):
        penulis = Profile.objects.get(user__username=self.kwargs["user"])
        self.queryset = penulis.post.filter(active=True)
        return super().get_queryset()

    def get_context_data(self, **kwargs):

        penulis = Profile.objects.get(user__username=self.kwargs["user"])
        self.kwargs.update({"penulis": penulis})

        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context["title"] = self.kwargs["user"]
        return context


class PostDetailView(ModelInstanceViewSeoMixin, HitCountDetailView, DetailView):
    model = Post
    template_name = "darisset/blog/blog-single.html"
    context_object_name = 'post'
    comment_form = CommentForm()
    count_hit = True
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        post = self.model.objects.get(slug=self.kwargs["slug"])

        comments = post.comments.filter(
            active=True, reply=None).order_by("-created")
        self.kwargs.update({'comments': comments})

        total_comments = post.comments.filter(active=True)
        self.kwargs.update({"total_comments": total_comments})

        self.kwargs.update({
        'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        })

        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context["comment_form"] = self.comment_form
        context["title"] = post.title
        return context


@login_required
def comment(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(
        active=True, reply=None).order_by("created")
    if request.method == "POST":
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            reply_id = request.POST.get('reply')
            comment_qs = None
            if reply_id:
                comment_qs = post.comments.get(id=reply_id)
            new_comment.reply = comment_qs
            new_comment.user = request.user.profile
            new_comment.post = post
            new_comment.save()
            messages.success(
                request, "Komentar dikirim! dan menunggu moderasi")
    return redirect("blog:detail", post.slug)


@login_required
def bookmark(request, id):
    post = get_object_or_404(Post, id=id)
    if post.bookmark.filter(id=request.user.profile.id).exists():
        post.bookmark.remove(request.user.profile.id)
    else:
        post.bookmark.add(request.user.profile.id)
    return redirect("blog:detail", post.slug)


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')
        if query is not None:
            lookups = Q(title__icontains=query) | Q(
                tags__name__icontains=query) | Q(category__icontains=query) | Q(slug__icontains=query)

            posts = Post.objects.filter(
                lookups).distinct().exclude(active=False)
            popular_posts = Post.objects.order_by('-hit_count_generic__hits')[:3]
            context = {
                'posts': posts,
                'submitbutton': submitbutton,
                'popular_posts': popular_posts,
                'title': 'Search',
            }
            return render(request, 'darisset/blog/search.html', context)
        else:
            return render(request, 'darisset/blog/search.html')
    else:
        return render(request, 'darisset/blog/search.html')
