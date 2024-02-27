from django.shortcuts import render
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from .models import Student
from django.shortcuts import get_object_or_404
import logging
from .utils import EmailThread
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings


logger = logging.getLogger('mylogger')

@api_view(http_method_names=('GET','POST'))
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_api(request):

    if request.method=='POST':
        try:
            serializer = StudentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('Product Created Successfull ')
            user_email = request.user.email
            subject ="Test Email"
            message ='User created SuccessFully'
            if user_email:
                EmailThread(
                    subject=subject,
                    message=message,
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]

                ).start()
                return Response(data={'details: EmailSend Successfully'})
            return Response(data=serializer.data,status=201)
        except:
            logger.error('Error to cerate record')
            return Response(data=serializer.errors,status=400)
    if request.method =='GET':
        try:
            obj = Student.objects.all()
            serializer= StudentSerializer(obj,many = True)
            logger.info('Data Fetch successfully...')
            return Response(data=serializer.data,status=204)
        except:
            logger.error('Error to fetch data')
            return Response(data=serializer.errors,status=404)

@api_view(http_method_names=('GET','POST','PUT','PATCH','DELETE'))
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def details_api(request,pk):
    obj = get_object_or_404(Student,pk=pk)
    if request.method == 'GET':
        try:
            serializer =StudentSerializer(obj)
            logger.info('Data retrived successfully')
            return Response(data=serializer.data,status=201)
        except:
            logger.error('error for data retriving')
            return Response(data=serializer.data,status=401)
    if request.method=='PUT':
        try:
            serializer=StudentSerializer(data=request.data,instance=obj)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('Data Updated Successfully...')
            user_email=request.user.email
            subject="Test Email"
            message='User updated successFully..'
            if user_email:
                EmailThread(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                ).start()

                return Response(data={'details':'Email Send SuccesFully'})
            return Response(data=serializer.data,status=201)
        except:
            logger.error('Error to update data')
            return Response(data=serializer.data,status=203)
    if request.method=='PATCH':
        try:
            serializer=StudentSerializer(data=request.data,instance=obj,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info('data updated succefully..')
            return Response(data=serializer.errors,status=205)
        except:
            logger.error('Error to update data...')
            return Response(data=serializer.data,status=405)
    if request.method=='DELETE':
        try:
            obj.delete()
            logger.info('Record is deleted successfully....')
            user_emial = request.user.email
            subject = "Test Email"
            message ='Úser Deleted Successfully..'
            if user_emial:
                EmailThread(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_emial]
                ).start()
                return Response(data={'details':'Email send Succwssfully..'})
            return Response(data=None,status=206)
        except:
            logger.info('error to delete data')
            return Response(data={'details':'NOT Found'},status=407)
        