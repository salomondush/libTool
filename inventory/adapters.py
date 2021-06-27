# from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

# project/users/adapter.py:
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from .models import User
from django.contrib.auth import logout
from .functions import get_user_emails

class HttpResponseRedirect(Exception):
    pass

allowed_emails = get_user_emails(User.objects.all())

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        u = sociallogin.user
        print(f"\n\n\n {u.email} \n\n\n")
        if u.email not in allowed_emails:
            logout(request)
            raise Http404("Ooops! Please login using the instituation email address with access! Please go back.")
          


# class CustomAccountAdapter(DefaultAccountAdapter):
#     def is_open_for_signup(self, request):
#         return False # No email/password signups allowed

# class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
#     def is_open_for_signup(self, request, sociallogin):
#         u = sociallogin.user
#         # Optionally, set as staff now as well.
#         # This is useful if you are using this for the Django Admin login.
#         # Be careful with the staff setting, as some providers don't verify
#         # email address, so that could be considered a security flaw.
#         #u.is_staff = u.email.split('@')[1] == "customdomain.com"
#         print(f"\n\n\n {u.email in allowed_emails}\n\n\n")
#         return u.email in allowed_emails