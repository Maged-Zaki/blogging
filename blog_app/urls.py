from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [ 
    path("", views.IndexView.as_view(), name='index'),
    path("login", views.LoginView.as_view(), name='login'),
    path("logout", LogoutView.as_view(), name='logout'),
    path("register", views.RegisterView.as_view(), name='register'),
    path("publish", views.PublishView.as_view(), name='publish'),
    path("article/<slug:slug>", views.ArticleView.as_view(), name='article'),
    path("my_articles", views.MyArticles.as_view(), name='my_articles'),
    path("all_articles", views.AllArticles.as_view(), name='all_articles'),
    path("search", views.search_results, name='search'),
    path("settings", views.SettingsView.as_view(), name='settings'),
    path("filter_all_articles", views.filter_all_articles, name='filter_all_articles'),
    path("filter_search_results", views.filter_search_results, name='filter_search_results'),
    path("change_password", views.change_password, name='change_password'),
    path("preview_article", views.preview_article, name='preview_article'),
    path("update_article/<slug:slug>", views.UpdateArticle.as_view(), name='update_article')


]