from django.contrib import admin


from .models import Article, Tag, Comment, UserProfile


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("user", "title")    


admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(UserProfile)
