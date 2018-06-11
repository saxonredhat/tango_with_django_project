from django.contrib import admin
from blog.models import *
from django import forms
from guardian.admin import GuardedModelAdmin
from image_cropping import ImageCroppingMixin

class UserInfoAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


admin.site.register(UserInfo, UserInfoAdmin)


class ArticleForm(forms.ModelForm):
    #content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Article
        fields = ('title', 'content', 'author', 'category', 'pulished_date', 'tags',)

    # class Media:
    #     js = (
    #         '/static/js/kindeditor/kindeditor-all.js',
    #         '/static/js/kindeditor/lang/zh-CN.js',
    #         '/static/js/kindeditor/config.js',
    #     )


class ArticleAdmin(GuardedModelAdmin):
    form = ArticleForm


# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Tag)