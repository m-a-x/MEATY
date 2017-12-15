from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from restapi import views

urlpatterns = [
    url(r'^group_members/$', views.MembersList.as_view()),
    url(r'^group_members/(?P<pk>[0-9]+)$', views.MembersDetail.as_view()),
    url(r'^posts/$', views.PostsList.as_view()),
    url(r'^posts/(?P<pk>[0-9]+)$', views.PostsDetail.as_view()),
    url(r'^schools/$', views.SchoolsList.as_view()),
    url(r'^schools/(?P<pk>[0-9]+)$', views.SchoolsDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
