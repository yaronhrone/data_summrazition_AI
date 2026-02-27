from django.contrib import admin

from articles import models

# Register your models here.
admin.site.register(models.Article)
admin.site.register(models.Summary)