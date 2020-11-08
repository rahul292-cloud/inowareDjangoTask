from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import status, viewsets
from django.http import Http404
from django.contrib.auth.models import User
from django.db.models import (Case, CharField, Count, DateTimeField,
                              ExpressionWrapper, F, FloatField, Func, Max, Min,
                              Prefetch, Q, Sum, Value, When, Subquery)
from dashboard.models import RegisterUser
from .serializers import *


class CreateUserRegister(CreateAPIView):
    parser_class = (FileUploadParser,)
    model = RegisterUser
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)  # Successful post

        response = 'Something Went Wrong !'
        if serializer.errors.get('email'):
            response = serializer.errors.get('email')[0]
        if serializer.errors.get('password'):
            response = serializer.errors.get('password')[0]
        if serializer.errors.get('userName'):
            response = serializer.errors.get('userName')[0]

        return Response({"Error":response}, status=status.HTTP_400_BAD_REQUEST)


class AppToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"Error": "Invalid Credentials!"}, status=status.HTTP_400_BAD_REQUEST)

class UserAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):

        registerUser = RegisterUser.objects.filter(userName=request.user).values('id', 'userId', 'userName',
                                                                     'name', 'photo',
                                                                     'email')

        if registerUser.exists():
            return Response(registerUser[0], status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)


class UserEditProfile(APIView):
    parser_class = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)
    def put(self, request, *args, **kwargs):

        instance = RegisterUser.objects.get(userName=request.user)

        serializer = userDetailsSerializers(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteProfile(APIView):
    # parser_class = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):

        registerUserInstance = RegisterUser.objects.get(userName=request.user)
        registerUserInstance.delete()
        userInstance = User.objects.get(username=request.user)
        userInstance.delete()
        return Response('Profile deleted', status=status.HTTP_200_OK)
