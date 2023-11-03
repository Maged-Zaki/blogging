from rest_framework.serializers import ModelSerializer, SerializerMethodField

from blog_app.models import Article, User

from datetime import datetime

class ArticleSerializer(ModelSerializer):
    date = SerializerMethodField(read_only=True)    # its a must to overwrite the date attr in the article
    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "tags",
            "slug",
            "image_link",
            "date",
        ]
    
    def get_date(self, object):
        return datetime.strftime(object.date, "%Y-%m-%d")
    

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields =["username", "password"]