from django.dispatch.dispatcher import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from .models import UserActivity

@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    print('user {} logged in through page {}'.format(user.username, request.META.get('HTTP_REFERER')))
    print (request.headers['user_agent'])