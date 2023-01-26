
from django.db import models

# Create your models here.  


class PJArticles(models.Model):
    title = models.CharField(max_length=50, verbose_name='Tytuł wpisu')
    description = models.CharField(max_length=100, verbose_name='Opis artykułu')
    content = models.TextField(null=False, verbose_name='Treść')
    pub_data = models.DateTimeField(verbose_name='Data Publikacji', auto_now_add=True)
    pub_user = models.CharField(verbose_name='Publikował - Inicjały', max_length=2)
    important = models.BooleanField(verbose_name='Czy ważny', default=0)
    image = models.ImageField(upload_to="img", verbose_name='Obrazek', null=True)
    status = models.BooleanField(verbose_name='Opublikowany?', default=0)

    def __str__(self):
        return self.title


class PJComments(models.Model):
    user = models.CharField(max_length=50, verbose_name='Użytkownik')
    comment = models.TextField(null=False, verbose_name='Komentarz')
    pub_data = models.DateTimeField(verbose_name='Data Publikacji', auto_now_add=True)
    article = models.ForeignKey(PJArticles, on_delete=models.PROTECT)

    def __str__(self):
        return self.comment