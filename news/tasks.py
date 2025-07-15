from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
import datetime




@shared_task
def send_notification_email(post_id, preview):
    from .models import Post, Category
    post = Post.objects.get(id=post_id)
    subscribers = set(post.postCategory.values_list('subscribers__email', flat=True))

    html_content = render_to_string('post_created_email.html', {'post': post, 'text': preview, 'link': f'{settings.SITE_URL}/post/news/{post_id}'})

    msg = EmailMultiAlternatives(
        subject=f'Новая статья: {post.title}',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def my_job():
    from .models import Post, Category
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string('daily_post.html', {'link': settings.SITE_URL, 'posts': posts})

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()