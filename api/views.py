from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.forms import model_to_dict


from blog_app.models import Article
from . serializers import ArticleSerializer, UserSerializer


""" GET API ways"""

# #using model to dict 
# @api_view(["GET"])
# def articles_api(request):
#     all_articles = Article.objects.all().order_by("-date")

#     data = []
#     for article in all_articles:
#         data.append(model_to_dict(article)) #change model to python dict then append to data list

#         tags = [tag.tag for tag in article.tags.all()]         #loop through tags of the article and access the tag object then the tag field and add it to a list

#         data[-1]['tags'] = tags            #set the value of tags in the article to the tags list
            
            
#     return Response(data)

# #using serializers
# @api_view(["GET"])
# def articles_api(request):    
#     all_articles = Article.objects.all().order_by("-date")

#     data = ArticleSerializer(all_articles, many=True).data
            
            
#     return Response(data)


# #using class to retrieve one instance
# class ArticleAPIView(generics.RetrieveAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer

#     # lookup_field = 'slug'   ##can be pk or slug or any other filed and pk is the default


# #using class to retrieve all instances
# class ArticleListAPIView(generics.ListAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer



"""POST API ways"""

@api_view(["POST"])
def create_article_api(request, *args, **kwargs):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        data = serializer.save()
    
        return Response("data saved!", status=200)
