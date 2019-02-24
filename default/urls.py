from . import views
from django.conf.urls import url
from django.conf import settings
# from django.conf.urls.static import static
from django.conf import  settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin/$', views.signin),
    url(r'^signup/$', views.signup),
    url(r'^home/$', views.home),
    url(r'^setting/$', views.uploadImg),
    # url(r'^setting/$', views.setting),
    url(r'^signout/$', views.signout),
    url(r'^hottopic/$', views.hottopic),
    url(r'^question/', views.question),
    url(r'^follow/', views.follow),
    url(r'^reply/', views.reply),
    url(r'^favorite/', views.favorite),
    url(r'^agree/', views.agree),
    # url(r'^comment/',views.comment),
    url(r'^upload/', views.uploadImg),
    url(r'^show/', views.showImg),

    url(r'^home/question_info/', views.question_info),
    url(r'^home/reply_info/', views.reply_info),
    url(r'^home/follow_info/', views.follow_info),
    url(r'^home/fav_info/', views.fav_info),
    url(r'^home/agree_info/', views.agree_info),
    url(r'^home/reply_msg/', views.reply_msg),
    url(r'^home/follow_msg/', views.follow_msg),
    url(r'^home/fav_msg/', views.fav_msg),
    url(r'^home/agree_msg/', views.agree_msg),

]
