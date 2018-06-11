# -*- coding:utf-8 -*-
from django import forms
from blog.models import *
from django.contrib.auth.models import User, Group , Permission ,ContentType
from django.utils.translation import ugettext, ugettext_lazy as _
from captcha.fields import CaptchaField
import mytools
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class ArticleForm(forms.ModelForm):
    type = forms.CharField(widget=forms.Select(choices=((1, '原创'), (2, '翻译'), (3, '转载'),)))

    class Meta:
        model = Article
        fields = ('title', 'type', 'content', 'category', 'tags')


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('website', 'picture','cropping')


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


class UserRegisterForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("两次输入的密码不匹配."),
        'password_length_short': _("密码长度不足8位."),
    }
    username = forms.CharField(label=_("用户名"))
    password1 = forms.CharField(label=_("密码"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("再次输入密码"),
                                widget=forms.PasswordInput)
    captcha = CaptchaField(label='验证码', required=True)
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
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('content',)



