from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ShortURL(models.Model):
    original_url = models.URLField(max_length=700)
    short_url = models.CharField(max_length=100)
    time_date_created = models.DateTimeField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.original_url