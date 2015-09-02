from django.conf import settings
from django.contrib.auth.models import User, check_password
from activity.models import CGUser
from activity import views

# from .models import Client
#
# class ClientAuthBackend(object):
#
#     def authenticate(self, username=None, password=None):
#         try:
#             user = Client.objects.get(email=username)
#             return user
#
#             if password == 'master':
#                 # Authentication success by returning the user
#                 return user
#             else:
#                 # Authentication fails if None is returned
#                 return None
#         except Client.DoesNotExist:
#             return None
#
#     def get_user(self, user_id):
#         try:
#             return Client.objects.get(pk=user_id)
#         except Client.DoesNotExist:
#             return None

def associate_by_email(**kwargs):
    print 'associate by email'
    print kwargs
    backend = kwargs['backend']

    # social = backend.strategy.storage.user
    # print social

    for value in kwargs['details']:
        print value, kwargs['details'][value]
    if backend.name == 'facebook':
        try:
            # print kwargs['backend']['name']
            email = kwargs['details']['email']
            if len(email):
                print email
                print user
                print views.user_exists(email)
                if 0 and (views.user_exists(email)):
                    user = CGUser.objects.get(email=email)
                    if not len(user.first_name):
                        user.first_name = kwargs['details']['first_name']
                    if not len(user.last_name):
                        user.first_name = kwargs['details']['last_name']
                    kwargs['user'] = CGUser.objects.get(email=email)
                # else:
                #     kwargs['user']['name'] = 'Rajeev'
        except :
            pass
    elif backend.name == 'google-oauth2':
        try:
            # print kwargs['backend']['name']
            email = kwargs['details']['email']
            kwargs['user'] = CGUser.objects.get(email=email)
            # kwargs['user']['name'] = 'Rajeev'
        except:
            pass
    return kwargs

def clear_users(**kwargs):
    print 'in clear users'
    # print kwargs

    backend = kwargs['backend']
    # social = backend.strategy.storage.user.get_social_auth(provider, uid)
    # social = backend.strategy.storage.user
    # allUser = ['55ce24a432d69a1e2a92a1c0']

    # for uid in allUser:
    #     print uid
        # social = backend.strategy.storage.user.get_social_auth(backend.name, uid)
        # print "user"
        # print social

    # print len(social.objects.all())
    print "end clear users"
    return kwargs
