from django.db import models


class MetaText(models.Model):
    name = models.CharField(max_length=200, default="coding")
    title = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=80)
    meta_description = models.CharField(max_length=160)
    meta_keywords = models.CharField(max_length=1000)
    meta_image = models.ImageField(upload_to ='main_site/')
    h1 = models.CharField(max_length=200, default="")
    h2 = models.CharField(max_length=200, default="")
    h3 = models.CharField(max_length=200, default="")
    h4 = models.CharField(max_length=200, default="")
    h5 = models.CharField(max_length=200, default="")
    h6 = models.CharField(max_length=200, default="")
    alt = models.TextField()

    def __str__(self):
        return self.title
