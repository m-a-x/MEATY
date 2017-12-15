# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend

from restapi.models import GroupMembers, Posts, Schools
from restapi.serializers import MemberSerializer, PostSerializer, SchoolSerializer
from rest_framework import generics


class MembersList(generics.ListCreateAPIView):
    queryset = GroupMembers.objects.all()
    serializer_class = MemberSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('school', 'date_added')


class MembersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupMembers.objects.all()
    serializer_class = MemberSerializer
    filter_backends = (DjangoFilterBackend, )


class PostsList(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('school', 'poster_name', 'post_date')


class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, )


class SchoolsList(generics.ListCreateAPIView):
    queryset = Schools.objects.all()
    serializer_class = SchoolSerializer
    filter_backends = (DjangoFilterBackend, )


class SchoolsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schools.objects.all()
    serializer_class = SchoolSerializer
    filter_backends = (DjangoFilterBackend, )
