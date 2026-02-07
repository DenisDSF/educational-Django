from django.shortcuts import render
from .services import get_news


def index(request):
    all_news = get_news()
    context = dict(all_news=all_news)
    return render(request, 'news/index.html', context=context)