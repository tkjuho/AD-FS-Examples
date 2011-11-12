from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import uuid

def hello(request):
    return HttpResponse("Hello world <Br/> <a href='http://localhost:8000/secret'> secret page </a> <br/> Authenticated: " + str(request.user.is_authenticated()))

@login_required
def secret(request):
    return HttpResponse('<a href="http://localhost:8000/">Front page</a><br/>Secret page')

def do_login(request):
    baseurl = 'https://ADFS-SERVER/adfs/ls/?wa=wsignin1.0'
    wtrealm ='&wtrealm=http%3a%2f%2flocalhost%3a8000%2f'  
    timestamp = datetime.now()
    wct = '&wct='+ str(timestamp.year) +'-'+str(timestamp.month).zfill(2)+'-' + str(timestamp.day).zfill(2)+ 'T'+str(timestamp.hour-2).zfill(2)+'%3a'+str(timestamp.minute).zfill(2)+'%3a'+str(timestamp.second).zfill(2)+'Z'
    loginurl = baseurl + wtrealm+wct    
    return redirect(loginurl)

@csrf_exempt
def SAML_handler(request):     
     # Enable SAML loggingif needed for debugging
     # SAML.log(logging.DEBUG, "PySAML.log")

     # The subject of the assertion. Usually an e-mail address or username.
     #subject = SAML.Subject(request.user.email,"urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress")

     # The authentication statement which is how the person is proving he really is that person. Usually a password.
     #authStatement = SAML.AuthenticationStatement(subject,"urn:oasis:names:tc:SAML:1.0:am:password",None)

     # Create a conditions timeframe of 5 minutes (period in which assertion is valid)
     #notBefore = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
     #notOnOrAfter = time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime(time.time() + 5))
     #conditions = SAML.Conditions(notBefore, notOnOrAfter)

     # Create the actual assertion
     #assertion = SAML.Assertion(authStatement, "Test Issuer", conditions)
     #return HttpResponse(assertion,  mimetype='text/xml')
     username = uuid.uuid4().hex[:30]
     try:
        while True:
            User.objects.get(username=username)
            username = uuid.uuid4().hex[:30]
     except User.DoesNotExist:
         pass
     user = authenticate(username=username, password="")     
     login(request,user)

     resp = '<a href="http://localhost:8000/">Front page</a><br/>' + str(request)
     return HttpResponse(resp)
