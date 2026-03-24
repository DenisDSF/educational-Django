from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages

from .forms import CommentForm
from .models import Article, Comment
from .services import get_news, get_article_comments


class IndexView(ListView):
    template_name = 'index.html'
    model = Article
    paginate_by = 10
    context_object_name = 'all_news'

    def get_queryset(self):
        return get_news()


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        paginate_by = 10
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page', 1)
        all_comments = get_article_comments(self.object.pk)
        paginator = Paginator(all_comments, paginate_by)
        current_page = paginator.get_page(page_number)

        context['form'] = CommentForm()
        context['comments'] = current_page
        context['is_paginated'] = current_page.has_other_pages()
        return context

def create_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if request.user.is_authenticated and not cleaned_data['is_anon']:
                user = request.user
                is_anon = False
            else:
                user = None
                is_anon = True
            comment = Comment(
                article_id=pk,
                user=user,
                is_anon=is_anon,
                text=cleaned_data['text']
            )
            comment.save()
            return redirect('article-detail', pk)
        else:
            for f in form:
                if f.errors:
                    messages.add_message(request, messages.ERROR, f.errors)
    return redirect('article-detail', pk)