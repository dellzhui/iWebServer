from django.apps import AppConfig
# from django.contrib import auth
# from django.contrib.auth.models import User, Group
# from django.shortcuts import get_object_or_404

# from boards.apps import Log


class MyaccountConfig(AppConfig):
    name = 'myaccount'


# class UserUtils:
#     def __init__(self, username, password):
#         try:
#             self.user = auth.authenticate(username=username, password=password)
#             if(self.user == None):
#                 Log.e('UserUtils:can not find user ' + str(username))
#         except Exception as err:
#             Log.e('UserUtils err:[' + str(err) + ']')
#             self.user = None
#
#     def get_user(self):
#         return self.user
#
#     def auto_login(self, request):
#         try:
#             if(self.user != None):
#                 auth.login(request, self.user)
#                 Log.d('login succeed')
#                 return True
#         except Exception as err:
#             Log.e('autologin err:[' + str(err) + ']')
#         return False
#
#     def add_user(self, username, password, email, usertype):
#         if (self.user == None):
#             return False, 'login failed'
#         if (not self.user.has_perm('boards.all_access')):
#             return False, 'no permission'
#         if (username != None and username != '' and password != None and password != ''):
#             try:
#                 User.objects.create_user(username=username, password=password, email=email)
#                 return self.set_user_type(username, usertype)
#             except Exception as err:
#                 Log.e('add_user err:[' + str(err) + ']')
#                 return False, str(err)
#
#     def delete_user(self, username):
#         if (self.user == None):
#             return False, 'login failed'
#         if (not self.user.has_perm('boards.all_access')):
#             return False, 'no permission'
#
#         try:
#             user = get_object_or_404(User, username=username)
#             if (user.is_superuser or user.has_perm('boards.all_access')):
#                 return False, 'can not delete admin user'
#             groups = Group.objects.filter(name='RegularGroup')
#             if (len(groups) == 1):
#                 group = groups[0]
#                 group.user_set.remove(user)
#             user.delete()
#             return True, 'succeed'
#         except Exception as err:
#             Log.e('delete_user err:[' + str(err) + ']')
#             return False, str(err)
#
#     def set_user_type(self, username, usertype):
#         if (self.user == None):
#             return False, 'login failed'
#         if (not self.user.has_perm('boards.all_access')):
#             return False, 'no permission'
#
#         try:
#             user = get_object_or_404(User, username=username)
#             if (usertype == None):
#                 return False, 'usertype err'
#
#             if (usertype == 'Regular' and not user.has_perm('boards.regular_access')):
#                 groups = Group.objects.filter(name='RegularGroup')
#                 if (len(groups) == 1):
#                     group = groups[0]
#                     group.user_set.add(user)
#                     return True, 'succeed'
#             elif (usertype == 'Guest' and user.has_perm('boards.regular_access')):
#                 groups = Group.objects.filter(name='RegularGroup')
#                 if (len(groups) == 1):
#                     group = groups[0]
#                     group.user_set.remove(user)
#                     return True, 'succeed'
#             return False, 'set usertype to ' + usertype + ' failed'
#         except Exception as err:
#             Log.e('set_user_type err:[' + str(err) + ']')
#             return False, str(err)
