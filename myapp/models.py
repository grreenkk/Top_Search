from django.db import models


class Search(models.Model):
    text = models.CharField(max_length=500)
    input_date = models.DateTimeField

    def __str__(self):
        return '{}'.format(self.text)

    class Meta:
        verbose_name_plural = 'Search'


# Create your models here.
