from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subscribe', views.sub_unsub, name='sub_page'),
    path('postBlog', views.postBlog, name='post_blog'),
    path('all_articles', views.all_articles, name='all_articles'),
    path('show_article/<int:articleId>', views.show_article, name='show_article'),
    path('send_email/<int:articleId>', views.send_email, name='send_email'),
]