from django.dispatch import receiver
from news.models import PostCategory, Post
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from project_news.settings import SITE_URL
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from allauth.account.signals import user_signed_up
from .tasks import send_notification_email


'''def send_notifications(preview, pk, title, subscribers):
    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/post/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()'''

@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        post_id = instance.pk   # Получаем ID поста
        post = Post.objects.get(id=post_id)  # Получаем сам пост
        preview = post.preview
        send_notification_email.delay(post_id, preview)


