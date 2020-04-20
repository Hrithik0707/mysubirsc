from django.shortcuts import render
from rest_framework.generics import CreateAPIView 
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import status,viewsets
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view

# Create your views here.

User = get_user_model()


from api.serializers import (
    UserCreateSerializer,
    UserLoginSerializer
    )

@api_view(['GET'])
def liveserver(request):
    context = "{'status':'OK'}"
    return Response(data=context,status= status.HTTP_200_OK)



class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def create(self,request,*args,**kwargs):
        return Response({'promptmsg':'You have succesfulyy registered.'})
# Create your views here.


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)