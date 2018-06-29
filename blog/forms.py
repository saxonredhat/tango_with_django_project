# -*- coding:utf-8 -*-
from django import forms
from blog.models import *
from django.contrib.auth.models import User, Group , Permission ,ContentType
from django.utils.translation import ugettext, ugettext_lazy as _
from captcha.fields import CaptchaField
from django.contrib.auth.hashers import check_password
import re
import mytools
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class ArticleForm(forms.ModelForm):
    error_messages = {
        'tags_too_many': _("请注意标签数量不能超过5个"),
        'category_value_error': _("请选择一个有效的文章分类"),
        'custom_category_value_error': _("请选择一个有效的个人分类"),
    }
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '文章标题'}),error_messages = {'required': "请注意文章标题不能为空"})
    type = forms.CharField(widget=forms.Select(choices=((1, '原创'), (2, '翻译'), (3, '转载'),)))
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '各个标签使用;或者,分隔,最多5个标签'}),error_messages = {'required': "请注意至少需要一个标签"})
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '请填写文章内容'}),error_messages = {'required': "请注意文章内容不能为空"})

    class Meta:
        model = Article
        fields = ('title', 'type', 'content', 'category','custom_category')
        error_messages = {
            'category': {
                'required': '请选择文章分类',
            },
            'custom_category': {
                'required': '请选择个人分类',
            },
        }

    def __init__(self, user, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['custom_category'].queryset = CustomCategory.objects.filter(user=user)

    def clean_tags(self):
        tag_list = re.split('[,;]',self.cleaned_data.get('tags'))
        if len(tag_list) > 5:
            raise forms.ValidationError(
                self.error_messages['tags_too_many'],
                code='tags_too_many',
            )
        return self.cleaned_data.get('tags')

    def clean_category(self):
        try:
            if not self.cleaned_data.get('category'):
                raise forms.ValidationError(
                    self.error_messages['category_value_error'],
                    code='category_value_error',
                )
            category = self.cleaned_data.get('category')
            category_obj=Category.objects.get(id=category.id)
            return category_obj
        except:
            raise forms.ValidationError(
                self.error_messages['category_value_error'],
                code='category_value_error',
            )

    def clean_custom_category(self):
        try:
            if not self.cleaned_data.get('custom_category'):
                raise forms.ValidationError(
                    self.error_messages['custom_category_value_error'],
                    code='custom_category_value_error',
                )
            print self.cleaned_data.get('custom_category')
            custom_category = self.cleaned_data.get('custom_category')
            custom_category_obj=CustomCategory.objects.get(id=custom_category.id)
            return custom_category_obj
        except:
            raise forms.ValidationError(
                self.error_messages['custom_category_value_error'],
                code='custom_category_value_error',
            )


class UserInfoForm(forms.ModelForm):
    picture = forms.ImageField(label=_('头像'), required=False, error_messages={'无效': _("仅图片文件")},
                     widget=forms.FileInput)
    class Meta:
        model = UserInfo
        fields = ('nickname','website', 'picture')


class UserBaseForm(forms.Form):
    username = forms.CharField(max_length=128, help_text="Please enter Username.")
    email = forms.EmailField(max_length=200, help_text="Please enter email.")


class UserAddForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("两次输入的密码不匹配."),
        'password_length_short': _("密码长度不足8位."),
    }
    username = forms.CharField(label=_("用户名"))
    password1 = forms.CharField(label=_("密码"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("再次输入密码"),
                                widget=forms.PasswordInput)
    email = forms.EmailField(label=_("邮箱"))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError(
                self.error_messages['password_length_short'],
                code='password_length_short',
            )
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserAddForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

        return user


class ChangePasswordForm(forms.ModelForm):
    error_messages = {
        'old_password_error': _("旧密码不正确"),
        'password_mismatch': _("两次输入的密码不匹配"),
        'password_length_short': _("密码长度不足8位"),
    }
    old_password = forms.CharField(label=_("旧密码"),
                                widget=forms.PasswordInput,error_messages = {'required': "旧密码不能为空"})
    password1 = forms.CharField(label=_("新密码"),
                                widget=forms.PasswordInput,error_messages = {'required': "新密码不能为空"})
    password2 = forms.CharField(label=_("再次确认密码"),
                                widget=forms.PasswordInput,error_messages = {'required': "确认密码不能为空"})
    class Meta:
        model = User
        fields = ('old_password', 'password1', 'password2')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password", None)
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['old_password_error'],
                code='old_password_error',
            )
        return old_password

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError(
                self.error_messages['password_length_short'],
                code='password_length_short',
            )
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


class NewEmailForm(forms.Form):
    new_email = forms.EmailField(label=_("新邮箱"))


class UserRegisterForm(forms.ModelForm):
    error_messages = {
        #'password_mismatch': _("两次输入的密码不匹配."),
        'password_length_short': _("密码长度不足8位."),
    }
    username = forms.CharField(label=_("用户名"))
    password1 = forms.CharField(label=_("密码"),widget=forms.PasswordInput)
    #password2 = forms.CharField(label=_("再次输入密码"),
    #                            widget=forms.PasswordInput)
    captcha = CaptchaField(label='验证码', required=True)
    email = forms.EmailField(label=_("邮箱"))

    class Meta:
        model = User
        fields = ('username', 'password1', 'email')

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError(
                self.error_messages['password_length_short'],
                code='password_length_short',
            )
        return password1

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError(
    #             self.error_messages['password_mismatch'],
    #             code='password_mismatch',
    #         )
    #     return password2

    # def save(self, commit=True):
    #     user = super(UserRegisterForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data['password1'])
    #     if commit:
    #         user.save()
    #
    #     return user


class UserEditForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("两次输入的密码不匹配."),
        'password_length_short': _("密码长度不足8位."),
    }
    password1 = forms.CharField(label=_("密码"),
                                widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label=_("再次输入密码"),
                                widget=forms.PasswordInput, required=False)
    email = forms.EmailField(label=_("邮箱"), required=False)
#    is_active = forms.ChoiceField(label=_("激活"),  widget=forms.CheckboxInput(), required=False)
#    is_superuser = forms.ChoiceField(label=_("管理员"), widget=forms.CheckboxInput(), required=False)

    class Meta:
        model = User
        fields = ('password1', 'password2', 'email')

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if password1:
            if len(password1) < 8:
                raise forms.ValidationError(
                    self.error_messages['password_length_short'],
                    code='password_length_short',
                )
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)


class PermissionForm(forms.ModelForm):
    error_messages = {
        'name_not_exist_chinese': _("名字中没检测到中文字符"),
    }
    content_types = [(x+'-'+y, x+' | '+y) for x, y in ContentType.objects.all().values_list('app_label', 'model')]
    app_label_model = forms.CharField(widget=forms.Select(choices=content_types))

    class Meta:
        model = Permission
        fields = ('name', 'codename',)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        for my_chr in unicode(name):
            if mytools.str_contain_chinese(my_chr):
                return name
        raise forms.ValidationError(
            self.error_messages['name_not_exist_chinese'],
            code='name_not_exist_chinese',
        )


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea,max_length=100)

    class Meta:
        model = Comment
        fields = ('content',)


class ForgetPasswordForm(forms.Form):
    errors_messages = {
        'username_not_exist': _("您输入的用户名不存在"),
    }
    username = forms.CharField(label=_("用户名"))
    error_css_class = "error"

    def clean_username(self):
        username = self.cleaned_data.get("username")
        get_user = User.objects.filter(username=username)
        if not get_user:
            raise forms.ValidationError(
                self.errors_messages['username_not_exist'],
                code='username_not_exist',
            )
        return username


