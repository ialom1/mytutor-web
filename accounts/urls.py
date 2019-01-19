from django.conf.urls import url
from django.contrib.auth import login, logout
from accounts import views

from accounts.forms import LoginForm

app_name = 'accounts'

urlpatterns = [
    url(r'^$', views.home, name='home_view'),
    url(r'^login/$', views.user_login, name='login_view'),
    url(r'^login_success/$', views.login_success, name='login_success'),
    url(r'^logout/$', views.user_logout, name='logout_view'),

    url(r'^register/$', views.register, name='register_view'),
    url(r'^register/userinfo/$', views.regprofile, name='user_info_view'),

    url(r'^studentprofile/$', views.student_profile, name='student_profile_view'),
    url(r'^studentprofile/(?P<pk>[0-9]+)/$', views.student_profile, name='student_profile_view_pk'),
    url(r'^edit-studentprofile/$', views.edit_student_profile, name='edit_student_profile_view'),

    url(r'^tutorprofile/$', views.tutor_profile, name='tutor_profile_view'),
    url(r'^tutorprofile/(?P<pk>[0-9]+)/$', views.tutor_profile, name='tutor_profile_view_pk'),
    url(r'^edit-tutorprofile/$', views.edit_tutor_profile, name='edit_tutor_profile_view'),

    url(r'^course-selection/$', views.course_selection, name='course_selection_view'),
    url(r'^course-selection/(?P<subject>\w+)/$', views.course_selection, name='course_selection_view_sub'),

    url(r'^tutor-search/$', views.tutor_search, name='tutor_search_view'),
    url(r'^tutor-search/(?P<subject>\w+)/$', views.tutor_search, name='tutor_search_view_sub'),

    url(r'^class-request/(?P<pk>[0-9]+)/$', views.class_request, name='class_request_view'),
    url(r'^tutor-messages/$', views.tutor_messages, name='tutor_messages_view'),
    url(r'^student-messages/$', views.student_messages, name='student_messages_view'),
]
