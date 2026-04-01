from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages

from .forms import CommentForm
from .models import Article, Comment
from .services import get_news, get_article_comments_text_and_username


class IndexView(ListView):
    template_name = 'index.html'
    model = Article
    paginate_by = 10
    context_object_name = 'all_news'

    def get_queryset(self):
        return get_news()


class ArticleDetailView(DetailView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        paginate_by = 10
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page', 1)
        all_comments = get_article_comments_text_and_username(self.object.pk)
        paginator = Paginator(all_comments, paginate_by)
        current_page = paginator.get_page(page_number)

        context['form'] = CommentForm()
        context['comments'] = current_page
        context['is_paginated'] = current_page.has_other_pages()
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Article,
            status=Article.Status.PUBLISH,
            pk=self.kwargs[self.pk_url_kwarg]
        )


class ArticleCreateCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = None

    def get_success_url(self):
        kwargs = {'pk': self.kwargs[self.pk_url_kwarg]}
        return reverse_lazy('article-detail', kwargs=kwargs)

    def form_valid(self, form):
        form.instance.article_id = self.kwargs['pk']
        cleaned_data = form.cleaned_data
        if self.request.user.is_authenticated and not cleaned_data['is_anon']:
            form.instance.user = self.request.user
            form.instance.is_anon = False
        elif self.request.user.is_authenticated and cleaned_data['is_anon']:
            form.instance.user = self.request.user
            form.instance.is_anon = True
        else:
            form.instance.user = None
            form.instance.is_anon = True
        messages.success(self.request, 'Комментарий добавлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        pk = self.kwargs[self.pk_url_kwarg]
        for f in form:
            if f.errors:
                messages.add_message(self.request, messages.ERROR, f.errors)
        return redirect('article-detail', pk)