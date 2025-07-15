from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Author
from django import forms

class PostFilter(FilterSet):
    author = ModelChoiceFilter(
        queryset=Author.objects.all(),  # Получение всех авторов из базы
        empty_label='Все авторы',  # Опция выбора "Все авторы"
        required=False  # Делаем это поле необязательным
    )

    date = DateFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
        }