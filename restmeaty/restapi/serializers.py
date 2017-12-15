from django.contrib.auth.models import User, Group

from restapi.models import GroupMembers, Posts, Schools
from rest_framework import serializers


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMembers
        fields = ('id', 'affil', 'fb_name', 'date_added',
            'school', 'school_name', 'approver_name')


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ('id', 'school', 'school_name', 'poster_name',
            'post_time', 'title', 'caption', 'price', 'num_reacts',
            'angrys', 'hahas', 'likes', 'loves', 'prides', 'sads',
            'thankfuls', 'wows', 'reacts_url', 'url', 'post_date',
            'post_hour', 'img_hash')


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schools
        fields = ['school_attended', 'school_posted', 'id', 'school_name']
