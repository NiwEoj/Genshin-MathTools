from django.db import models

# Create your models here.
class Weapon(models.Model):
    name        = models.TextField(max_length=100)
    pic         = models.TextField(default="none")
    type        = models.IntegerField()
    passive     = models.TextField(default="none")
    attack      = models.FloatField(default=0)
    statTitle   = models.TextField(null=True, default="none")
    stat        = models.FloatField(default=0)
