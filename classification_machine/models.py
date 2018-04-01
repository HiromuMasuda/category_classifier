from django.db import models

class Article(models.Model):

    ENTERTAINMENT = 1
    SPORTS        = 2
    OMOSHIRO      = 3
    DOMESTIC      = 4
    INTERNATIONAL = 5
    COLUMN        = 6
    IT_SCIENCE    = 7
    GOURMET       = 8

    title = models.CharField(max_length=256)
    content = models.CharField(max_length=8192)
    category = models.IntegerField()
    updated_at = models.DateTimeField()
