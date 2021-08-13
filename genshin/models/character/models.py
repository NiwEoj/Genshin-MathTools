from django.db import models

class Character(models.Model):
    name        = models.TextField(max_length=100)
    hp          = models.FloatField()
    attack      = models.FloatField()
    defence     = models.FloatField()
    em          = models.FloatField()
    stamina     = models.FloatField()
    critRate    = models.FloatField()
    critDmg     = models.FloatField()
    selfHeal    = models.FloatField()
    othersHeal  = models.FloatField()
    recharge    = models.FloatField()
    cdReduction = models.FloatField()
    shield      = models.FloatField()

    pyroDmg     = models.FloatField()
    pyroRes     = models.FloatField()
    hydroDmg    = models.FloatField()
    hydroRes    = models.FloatField()
    dendroDmg   = models.FloatField()
    dendroRes   = models.FloatField()
    electroDmg  = models.FloatField()
    electroRes  = models.FloatField()
    anemoDmg    = models.FloatField()
    anemoRes    = models.FloatField()
    cryoDmg     = models.FloatField()
    cryoRes     = models.FloatField()
    geoDmg      = models.FloatField()
    geoRes      = models.FloatField()
    physDmg     = models.FloatField()
    physRes     = models.FloatField()