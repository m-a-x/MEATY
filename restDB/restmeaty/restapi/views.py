# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404

from restapi.models import GroupMembers, Posts, Schools
from restapi.serializers import MemberSerializer, PostSerializer, SchoolSerializer
from rest_framework import generics


class MembersList(generics.ListCreateAPIView):
    queryset = GroupMembers.objects.all()
    serializer_class = MemberSerializer
    filter_fields = ('school', 'date_added')


class MembersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupMembers.objects.all()
    serializer_class = MemberSerializer


class PostsList(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    filter_fields = ('school', 'poster_name', 'post_date')


class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer


class SchoolsList(generics.ListCreateAPIView):
    queryset = Schools.objects.all()
    serializer_class = SchoolSerializer


class SchoolsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schools.objects.all()
    serializer_class = SchoolSerializer
