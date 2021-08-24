from django.db import models

# Create your models here.
class Artifact(models.Model):
    name         = models.TextField(max_length=100)
    twopcEffect  = models.TextField(default="none")
    fourpcEffect = models.TextField(default="none")
    element      = models.TextField(default="none")
    twopcBonus   = models.TextField(default="none")
    twopcStats   = models.FloatField(default="none")
    fourpcBonus  = models.TextField(default="none")
