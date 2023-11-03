from django.urls import path

from . import views

urlpatterns = [
    # path('all_articles', views.articles_api)
    # path('article/<slug:slug>', views.ArticleAPIView.as_view())  #to get one article
    # path('all_articles', views.ArticleListAPIView.as_view())  #to get one article
    path('create_article', views.create_article_api)  #to create article
]