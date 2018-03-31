from django.db import models

class Article(models.Model):

    ENTERTAINMENT = 0
    SPORTS        = 1
    OMOSHIRO      = 2
    DOMESTIC      = 3
    INTERNATIONAL = 4
    COLUMN        = 5
    IT_SCIENCE    = 6
    GOURMET       = 7

    title = models.CharField(max_length=256)
    content = models.CharField(max_length=8192)
    category = models.IntegerField()
    updated_at = models.DateTimeField()
