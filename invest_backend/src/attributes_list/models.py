from django.db import models


class Portfolio(models.Model):
    name = models.CharField(max_length=30)
