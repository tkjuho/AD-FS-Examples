from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import uuid

# The front page
def hello(request):
    return HttpResponse("Hello world <Br/> <a href='http://localhost:8000/secret'> secret page </a> <br/> Authenticated: " + str(request.user.is_authenticated()))

# secret content
@login_required
def secret(request):
    return HttpResponse('<a href="http://localhost:8000/">Front page</a><br/>Secret page')

# This does the actual login...
# ... and looks ugly
def do_login(request):
    baseurl = 'https://ADFS-SERVER/adfs/ls/?wa=wsignin1.0'
    wtrealm ='&wtrealm=http%3a%2f%2flocalhost%3a8000%2f'  
    timestamp = datetime.now()
    wct = '&wct='+ str(timestamp.year) +'-'+str(timestamp.month).zfill(2)+'-' + str(timestamp.day).zfill(2)+ 'T'+str(timestamp.hour-2).zfill(2)+'%3a'+str(timestamp.minute).zfill(2)+'%3a'+str(timestamp.second).zfill(2)+'Z'
    # Constructing the request url
    loginurl = baseurl + wtrealm+wct    
    return redirect(loginurl)

# Handles the response from AD FS (actually now just logs in if anything comes)
@csrf_exempt
def SAML_handler(request):     
     # Unique user created each time
     username = uuid.uuid4().hex[:30]
     try:
        while True:
            User.objects.get(username=username)
            username = uuid.uuid4().hex[:30]
     except User.DoesNotExist:
         pass
     # Aut & login (required order), auth goes to fake authentication
     user = authenticate(username=username, password="")     
     login(request,user)

     resp = '<a href="http://localhost:8000/">Front page</a><br/>' + str(request)
     return HttpResponse(resp)
