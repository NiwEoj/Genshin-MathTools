from django.db import models

class Character(models.Model):
    name        = models.TextField(max_length=100)
    pic         = models.TextField(default="")
    user        = models.IntegerField(default=1) # 1 - sword, 2 - claymore, 3 - polearm, 4 - catalyst, 5 - bow
    element     = models.IntegerField(default=1) # 1 - pyro, 2 - hydro, 3 - dendro, 4 - electro, 5 - anemo, 6 - cryo, 7 - geo
    hp          = models.TextField(default="[]")
    attack      = models.TextField(default="[]")
    defence     = models.TextField(default="[]")
    em          = models.FloatField(default=0.0)
    stamina     = models.FloatField(default=0.0)
    critRate    = models.FloatField(default=0.0)
    critDmg     = models.FloatField(default=0.0)
    selfHeal    = models.FloatField(default=0.0)
    othersHeal  = models.FloatField(default=0.0)
    recharge    = models.FloatField(default=1.0)
    cdReduction = models.FloatField(default=0.0)
    shield      = models.FloatField(default=0.0)

    pyroDmg     = models.FloatField(default=0.0)
    pyroRes     = models.FloatField(default=0.0)
    hydroDmg    = models.FloatField(default=0.0)
    hydroRes    = models.FloatField(default=0.0)
    dendroDmg   = models.FloatField(default=0.0)
    dendroRes   = models.FloatField(default=0.0)
    electroDmg  = models.FloatField(default=0.0)
    electroRes  = models.FloatField(default=0.0)
    anemoDmg    = models.FloatField(default=0.0)
    anemoRes    = models.FloatField(default=0.0)
    cryoDmg     = models.FloatField(default=0.0)
    cryoRes     = models.FloatField(default=0.0)
    geoDmg      = models.FloatField(default=0.0)
    geoRes      = models.FloatField(default=0.0)
    physDmg     = models.FloatField(default=0.0)
    physRes     = models.FloatField(default=0.0)

    ascStat     = models.TextField(default="")
    ascension   = models.TextField(default="[]")