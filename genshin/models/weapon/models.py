from django.db import models

# Create your models here.
class Weapon(models.Model):
    name        = models.TextField(max_length=100)
    pic         = models.TextField(default="none")
    rarity      = models.IntegerField(default=1)
    type        = models.IntegerField()
    passive     = models.TextField(default="none")
    attack      = models.TextField(default="[]")
    statTitle   = models.TextField(null=True, default="none")
    stat        = models.TextField(default="[]")
