from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(blank=True,unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)

    class Meta:
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
