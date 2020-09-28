from django.urls import path

from .views import PostDetailView, bookmark, comment, CategoryView, TagView, search, PopularView, PenulisView, BookmarkView, contactView, successView

app_name = "blog"

urlpatterns = [
    path("post/<str:slug>/", PostDetailView.as_view(), name="detail"),
    path("bookmark/<int:id>/", bookmark, name="bookmark"),
    path("comment/<str:slug>/", comment, name="comment"),
    path("category/<str:category>/", CategoryView.as_view(), name="category"),
    path("tags/<str:tag>/", TagView.as_view(), name="tag"),
    path("penulis/<str:user>/", PenulisView.as_view(), name="penulis"),
    path("bookmarks/", BookmarkView.as_view(), name="bookmarks"),
    path("search/", search, name="search"),
    path("popular/", PopularView.as_view(), name="popular"),
    # path("bookmark/", bookmark, name="book"),
]
