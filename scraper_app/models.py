from django.db import models


class Scraper(models.Model):
    url = models.URLField(max_length=200)
    steps = models.TextField()  # This might be a JSONField depending on your steps structure
    case = models.CharField(max_length=200) 
    data = models.CharField(max_length=200)

    def __str__(self):
        return self.url

