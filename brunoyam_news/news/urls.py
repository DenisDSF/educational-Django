from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import IndexView, ArticleDetailView, create_comment

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path(
        'articles/<int:pk>/',
        ArticleDetailView.as_view(),
        name='article-detail'
    ),
    path(
        'articles/<int:pk>/add_comment',
        create_comment,
        name='article-add-comment'
    )
]

if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))