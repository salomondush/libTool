# from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import Http404

# project/users/adapter.py:
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


allowed_emails = [ #TODO: setup a user model in database for allowed users
    "salomon.dushimirimana@vanderbilt.edu"
]

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        u = sociallogin.account.user
        if u.email not in allowed_emails:
            raise Http404("Please login using the instituation email address with access!")


# class MyAccountAdapter(DefaultAccountAdapter):

#     def get_login_redirect_url(self, request):
#         path = "/{url}"
#         print(f"\n\n {request.path} \n\n")
#         return path.format(url = request.path)
           