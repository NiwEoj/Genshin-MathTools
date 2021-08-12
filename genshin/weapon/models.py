from django.db import models

class Weapon(models.Model):
    name        = models.TextField(max_length=100)
    type        = models.IntegerField()
    passive     = models.TextField(null=True)
    minAtt      = models.FloatField()
