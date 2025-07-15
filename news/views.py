from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.http import HttpResponse
from django.views import View
from django.utils.translation import gettext as _
import pytz


class Index(View):
    def get(self, request):
        string = _('Hello world')
        models = Post.objects.all()
        categories = Category.objects.all()
        comments = Comment.objects.all()
        current_time = timezone.now()

        context = {
            'string': string,
            'models': models,
            'categories': categories,
            'comments': comments,
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        }
        return HttpResponse(render(request, 'index.html', context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class NewsSearch(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context

class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'

    def form_valid(self, form):
        today = timezone.now().date()
        news_count = Post.objects.filter(author=self.request.user.author, dateCreation__date=today).count()
        if news_count >= 3:
            form.add_error(None, 'Нельзя публиковать больше 3 новостей за сутки!')
            return self.form_invalid(form)
        form.instance.categoryType = Post.NEWS
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.pk])

class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'

    def form_valid(self, form):
        form.instance.categoryType = Post.ARTICLE
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.pk])

class NewsUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'

    def form_valid(self, form):
        form.instance.categoryType = Post.NEWS
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.pk])

class ArticleUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'

    def form_valid(self, form):
        form.instance.categoryType = Post.ARTICLE
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.pk])

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку постов категории '
    return render(request, 'subscribe.html', {'category': category, 'message': message})






