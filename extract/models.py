from django.db import models
import datetime
from django.utils import timezone


class Keyword(models.Model):
    keyword  = models.CharField(max_length=30)
    def __str__(self):
        return self.keyword

class StopWord(models.Model):
    stop_word  = models.CharField(max_length=30)
    def __str__(self):
        return self.stop_word
        



