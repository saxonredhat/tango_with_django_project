from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(blank=True,null=False,unique=True)
    likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'page'


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        db_table = 'userprofile'


class City(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey('Province', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'city'


class District(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'district'


class Province(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'province'


class Town(models.Model):
    name = models.CharField(max_length=50)
    district = models.ForeignKey(District, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'town'


class Village(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    town = models.ForeignKey(Town, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'village'


class Zone(models.Model):
    province = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    town = models.CharField(max_length=50, blank=True, null=True)
    village = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zone'
        unique_together = (('province', 'city', 'district', 'town', 'village'),)


class Zone2(models.Model):
    pro = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    dist = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zone2'
        unique_together = (('pro', 'city', 'dist'),)

