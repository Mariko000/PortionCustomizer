# profanity_filter/models.py

from django.db import models

class NgWord(models.Model):
    word = models.CharField(max_length=255, unique=True, verbose_name='NGワード')

    def __str__(self):
        return self.word