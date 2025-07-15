from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_notification_email


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        postRating = self.post_set.all().aggregate(postSum=Sum('rating'))
        pRating = 0
        pRating += postRating.get('postSum')

        commentRating = self.authorUser.comment_set.all().aggregate(commentSum=Sum('rating'))
        cRating = 0
        cRating += commentRating.get('commentSum')

        self.ratingAuthor = pRating * 3 + cRating
        self.save()

    def __str__(self):
        return self.authorUser.username

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    @property
    def preview(self):
        return self.text[0:50] + '...'

    def __str__(self):
        return f'{self.title.title()}: {self.text[:100]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

'''@receiver(post_save, sender=Post)
def send_new_post_notification(sender, instance, created, **kwargs):
    if created:
        send_notification_email.delay(instance.id)'''


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.post.title} | {self.category.name}'

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.commentUser.username

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

