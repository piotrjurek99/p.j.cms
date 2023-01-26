from django.contrib import admin
from django.db import models
from pjarticles.models import PJArticles, PJComments
# Register your models here.

modules = [PJArticles, PJComments]
admin.site.register(modules)