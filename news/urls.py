from django.urls import path
# Импортируем созданное нами представление
from .views import (PostList, PostDetail, NewsSearch, NewsCreateView, ArticleCreateView, NewsUpdateView, ArticleUpdateView, PostDelete,
                    CategoryListView, subscribe, Index)


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('news/', PostList.as_view(), name='post_list'),
   path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/search', NewsSearch.as_view()),
   path('news/create', NewsCreateView.as_view(), name='news_create'),
   path('articles/create', ArticleCreateView.as_view(), name='article_create'),
   path('news/<int:pk>/edit', NewsUpdateView.as_view(), name='news_update'),
   path('articles/<int:pk>/edit', ArticleUpdateView.as_view(), name='article_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('', Index.as_view(), name='index'),
]

