# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Schools(models.Model):

    school_name = models.CharField(max_length=15, unique=True)

    class Meta:
        db_table = "schools"


class GroupMembers(models.Model):

    id = models.IntegerField(primary_key=True)
    affil = models.CharField(max_length=250, blank=True, null=True)
    fb_name = models.CharField(max_length=100)
    date_added = models.DateField()
    school = models.CharField(max_length=15)
    school_name = models.ForeignKey("Schools",
        on_delete=models.CASCADE,
        related_name="school_attended",
        to_field="school_name"
    )
    approver_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'group_members'


class Posts(models.Model):

    id = models.CharField(primary_key=True, max_length=12)
    school = models.CharField(max_length=15)
    school_name = models.ForeignKey("Schools",
        on_delete=models.CASCADE,
        related_name="school_posted",
        to_field="school_name"
    )
    poster_name = models.CharField(max_length=100)
    post_time = models.DateTimeField()
    title = models.CharField(max_length=110, blank=True, null=True)
    caption = models.CharField(max_length=2000, blank=True, null=True)
    price = models.CharField(max_length=75, blank=True, null=True)
    num_reacts = models.IntegerField(blank=True, null=True)
    angrys = models.IntegerField(blank=True, null=True)
    hahas = models.IntegerField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    loves = models.IntegerField(blank=True, null=True)
    prides = models.IntegerField(blank=True, null=True)
    sads = models.IntegerField(blank=True, null=True)
    thankfuls = models.IntegerField(blank=True, null=True)
    wows = models.IntegerField(blank=True, null=True)
    reacts_url = models.CharField(max_length=120, blank=True, null=True)
    url = models.CharField(max_length=120, blank=True, null=True)
    post_date = models.DateField()
    post_hour = models.IntegerField(blank=True, null=True)
    img_hash = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'posts'
