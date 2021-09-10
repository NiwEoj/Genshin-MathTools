from django.db import models
from django.utils.translation import to_language

# Create your models here.
class Artifact(models.Model):
    name         = models.TextField(max_length=100)
    tag          = models.TextField(default='short form')
    rarity       = models.IntegerField(default=5)
    twopcElement = models.TextField(default="none")
    twopcEffect  = models.TextField(default="none")
    fourpcEffect = models.TextField(default="none")
    twopc        = models.TextField(default="none")
    fourpc       = models.TextField(default="none")
    twopcStats   = models.FloatField(default="none")
    fourpcStats  = models.TextField(default="none")
    fourpcStacks = models.TextField(default="none")
    fourpcReactT = models.TextField(default="none")
