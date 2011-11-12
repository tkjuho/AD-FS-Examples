from django.conf import settings
from django.contrib.auth.models import User, check_password

class fakeAuth(object):    
    def authenticate(self, username=None, password=None):
        user = User(username=username, password=password)        
        return user
        

    def get_user(self, user_id):
        return User(username=user_id, password='123')        
        
