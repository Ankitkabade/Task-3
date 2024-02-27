from django.shortcuts import render
from rest_framework.decorators import api_view
import logging
from rest_framework.response import Response
from .serializers import UserSerializer,User
from django.conf import settings
from activation.utils import EmailThread
from activation.tokens import account_activation_token
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode







logger =logging.getLogger('mylogger')

@api_view(http_method_names=(['POST']))
def user_api(request):
    if request.method=='POST':
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj=serializer.save()
            obj.is_active=False
            obj.save()
            
            domain = get_current_site(request=request).domain
            
            token =account_activation_token.make_token(obj)
            
            uid = urlsafe_base64_encode(force_bytes(obj.pk))
            
            relative_url = reverse('activate',kwargs={'uid':uid,'token':token})
            
            absolute_url = 'http://%s'%(domain+relative_url,)
            
            message = "Hello %s,\n\t Thank you for creating account with us. Please click on the link below"\
            "to active your account\n %s"%(obj.username,absolute_url)
            subject="Account Activation Email"
            EmailThread(subject=subject,message=message,recipient_list=[obj.email],from_email=settings.EMAIL_HOST_USER).start()
            return Response({'Message':'please check your email for account activation mail'},status=201)
        except Exception as e:
            print(e)
            logger.error('error to creating  user')
            return Response(data=serializer.errors,status=404)
        
def userAccountActivate(request,uid,token):

    if request.method=='GET':
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk= user_id)
        except(TypeError,ValueError,OverflowError,User.DoesNotExist)as e:
            return Response(data={'details':'there is an error'},status=400)
        if account_activation_token.check_token(user=user,token=token):
            user.is_active=True
            user.save()
            return Response(data={'details':'Account Activated SuccessFully'},status=200)
        return Response(data={'details':'Account link Invalid'},status=400)
