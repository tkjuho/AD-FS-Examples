from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from datetime import datetime
from django.conf import settings

def hello(request):
    return HttpResponse("Hello world <Br/> <a href='secret'> secret page </a>")

@login_required
def secret(request):
    return HttpResponse("Secret page")

def login(request):
    baseurl = 'https://ADFS_URL/adfs/ls/?wa=wsignin1.0'
    wtrealm ='&wtrealm=http%3a%2f%2flocalhost%3a8000%2f'
    #wctx = '&wctx=rm%3d0%26id%3dpassive%26ru%3d%252fPortalApp'
    timestamp = datetime.now()
    wct = '&wct='+ str(timestamp.year) +'-'+str(timestamp.month)+'-' + str(timestamp.day)+ 'T'+str(timestamp.hour-2)+'%3a'+str(timestamp.minute)+'%3a'+str(timestamp.second)+'Z'
    loginurl = baseurl + wtrealm +wct
    return redirect(loginurl)

def SAML_handler(request):
    return HttpResponse("Got some")
