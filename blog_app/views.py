from typing import Any, Dict, Optional, Type
from django.db.models.query import QuerySet
from django.forms.forms import BaseForm
from django.forms.models import BaseModelForm
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, View, FormView, DetailView, ListView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied



from markdown2 import Markdown
import json


from .models import Article, Comment, UserProfile, Tag
from .forms import LoginForm, CreateUserForm, PublishForm


# Create your views here.


class IndexView(TemplateView):
    template_name = "blog_app/index.html"


class LoginView(FormView):

    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        
        user = authenticate(username=username, password=password)

    
        if user is not None:
            login(self.request, user)
        else:
            username_exists = User.objects.filter(username=username).exists()

            if username_exists:
                form.add_error("password", "Invalid Password")
                return super().form_invalid(form)
            else:
                form.add_error("username", "Username incorrect")
                return super().form_invalid(form)
            
        if self.request.POST.get("remeber_me"):
            self.request.session.set_expiry(2592000) #30days
        else:
            self.request.session.set_expiry(0) #until user closes the browser
            
        return super().form_valid(form)


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = CreateUserForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        response = super().form_valid(form)

        #Create userprofile so later can access it and change profile picture without errors
        user_profile = UserProfile(user=self.object)
        user_profile.save()

        login(self.request, self.object)

        messages.success(self.request, "Registered Sucessfully")

        return response


    
class PublishView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")

    template_name = "blog_app/publish.html"
    form_class = PublishForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("article", args=[self.object.slug])


def preview_article(request):
    data  = json.loads(request.body.decode('utf-8'))
    article_content = data.get("article_content", "")

    markdowner = Markdown()

    converted_article_content = markdowner.convert(article_content)
    
    return JsonResponse({"article_preview_content": converted_article_content})


class UpdateArticle(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("login")

    template_name = "blog_app/update_article.html"
    model = Article
    fields = ("title", "content", "tags", "slug", "image_link")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_object = User(id=self.request.user.id)

        get_object_or_404(Article, user=user_object, id=self.object.id)

        return context
    
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["image_link"].required = False

        return form

    def get_success_url(self):
         return reverse("article", args=[self.object.slug])
    


class ArticleView(View):

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)

        markdowner = Markdown()
        article.content = markdowner.convert(article.content)

        comments = article.comments.all().order_by("-date")

        return render(request, "blog_app/article.html", {"article": article, "comments": comments})

    def post(self, request, slug):
        comment = request.POST["comment"]

        article = get_object_or_404(Article, slug=slug)
        user = request.user

        user_comment = Comment(user=user, comment=comment, article=article)
        user_comment.save()

        return HttpResponseRedirect(reverse("article", args=[article.slug]))
    


class MyArticles(ListView):
    template_name = "blog_app/my_articles.html"
    model = Article
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user).order_by("-date")
        

class AllArticles(ListView):
    template_name = "blog_app/all_articles.html"
    model = Article
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.all().order_by("-date")
    
    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()

        return context
    
        
    
def filter_all_articles(request):
    tag = request.GET.get("tag")

    try:
        tag_object = Tag.objects.get(tag=tag)
        filtered_articles = Article.objects.filter(tags=tag_object).order_by("-date")
    except:
        filtered_articles = Article.objects.all().order_by("-date")
        



    return render(request, "blog_app/all_articles.html", {"articles": filtered_articles, "tags": Tag.objects.all(), "selected_tag": tag})
        

def search_results(request):
    query = request.GET["q"]
    search_results = Article.objects.filter(title__icontains=query).order_by("-date")

    return render(request, "blog_app/search_results.html", {"search_results": search_results, "query": query, "tags": Tag.objects.all()})


def filter_search_results(request):
    query = request.GET.get("q")
    tag = request.GET.get("tag")

    try:
        tag_object = Tag.objects.get(tag=tag)
    except:
        return HttpResponseRedirect("/search?q=")

    search_results = Article.objects.filter(title__icontains=query)

    filtered_search_results = search_results.filter(tags=tag_object)

    return render(request, "blog_app/search_results.html", {"search_results": filtered_search_results, "tags": Tag.objects.all(), "query": query})


class SettingsView(LoginRequiredMixin,View):
    login_url = reverse_lazy("login")

    def get(self, request):
        form = CreateUserForm(instance=request.user)

        return render(request, "blog_app/settings.html", {"form": form})
    
    def post(self, request):
        profile_image = request.FILES.get("profile_image")
        username = request.POST.get("username")

        form = CreateUserForm(instance=request.user)

        if profile_image:
            if not profile_image.content_type.startswith('image'):
                form.add_error("image", "Invalid image")
                return render(request, "blog_app/settings.html", {"form": form})
            else:
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.profile_image = profile_image
                user_profile.save()
                messages.success(request, "Profile picture has been updated")
                
        if username:

            user_check = User.objects.filter(username=username).first()

            if user_check:
                if request.user == user_check:
                    return HttpResponseRedirect(reverse("settings"))
                else:
                    messages.warning(request, "Username already exists")
                    return render(request, "blog_app/settings.html", {"form": form})      
            else:
                current_user = User.objects.get(id=request.user.id)
                current_user.username = username
                current_user.save()
                messages.success(request, "Username has been updated")

            
        return HttpResponseRedirect(reverse("settings"))
    
def change_password(request):
    current_password = request.POST.get("current_password")
    new_password = request.POST.get("new_password")
    new_password_again = request.POST.get("new_password_again")

    if not current_password or not new_password or not new_password_again:
        messages.warning(request, "All fields required")
        return HttpResponseRedirect(reverse("settings"))
    
    password_authenticate =  authenticate(username=request.user.username, password=current_password)

    if password_authenticate:
        if new_password != new_password_again:
            messages.warning(request, "New passwords must match!")
            return HttpResponseRedirect(reverse("settings"))

        else:
            password_hashed = make_password(new_password)
            user = User.objects.get(id=request.user.id)
            user.password = password_hashed
            user.save()
            login(request, user)
            
            messages.success(request, "Password has been changed")
            return HttpResponseRedirect(reverse("settings"))
    else:
        messages.warning(request, "Invalid current password ")

    return HttpResponseRedirect(reverse("settings"))





    

