from django.http import HttpResponse
from django.shortcuts import render
from news.models import Article

def index(request):
    main_news = Article.objects.all()[0]
    context = dict(main_news=main_news)
    return render(request, 'news/index.html', context=context)