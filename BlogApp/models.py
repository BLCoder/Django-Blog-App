from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.


class category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_category_url(self):
        #return '/category/%s'%self.id
        return reverse('category',kwargs={'pk':self.pk})


class article(models.Model):
    article_author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    image=models.FileField()
    posted_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.title
    def get_single_url(self):
        return '/article/%s'%self.id

    def get_author_post(self):
        return reverse('author',kwargs={'name':self.article_author.name}) 