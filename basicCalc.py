import matplotlib.pyplot as plt
from numpy import empty
import seaborn as sns
import random as rd
import timeit
import pandas as pd
sns.set_style("darkgrid")

start = timeit.default_timer()

def resCalc(enemres,resreduc):
    resmulti = enemres - resreduc
    if resmulti < 0:
        resmulti = 1 - (resmulti / 2)
    elif resmulti < .75:
        resmulti = 1 - resmulti
    else:
        resmulti = 1 / (4 * resmulti + 1)
    return resmulti

# load base info/stats 
reaction = 'vape'
lvmulti = 723                   # lvmulti is base dmg of transformative reaction 
chrlv,chratk = (90,244)
asccrit,asccdmg,ascatk,ascem,ascdef,aschp,ascdmgbns = (0,0,.24,0,0,0,0)
wpnatk,wpncrit,wpncdmg,wpnatkp,wpnem = (510,0,0,.413,0)
wpndmgbns = 0
artcrit,artcdmg,artatk,artem,artdef,arthp,artdmgbns = (.55,.7,.7,0,0,0,.466)
artflower,artfeather = (4780,311)
resreducA,resreducT,resreducP = (0,0,0)
defreduc = 0
enemlv = 90
enemresA,enemresT,enemresP = (.1,.1,.1)

# process stats for later use
baseatk = wpnatk + chratk
ttlatkp = ascatk + artatk + wpnatkp
ttlcrit = .05 + asccrit + wpncrit + artcrit
ttlcdmg = .5 + asccdmg + wpncdmg + artcdmg
ttlem = ascem + wpnem +  artem
ttldmgbns = artdmgbns + wpndmgbns
atkstt = baseatk * ttlatkp + artfeather
critmulti = 1 + ttlcrit * ttlcdmg
dmgmulti = 1 + ttldmgbns 
if reaction == 'vape':
    reactmulti = 1.5 
    tdmg = 0
elif reaction =='melt':
    reactmulti = 2 
    tdmg = 0
elif reaction == 'ov':
    reactmulti = 1
    tdmg = lvmulti * 4
elif reaction == 'ec':
    reactmulti = 1
    tmdg = lvmulti * 4.8
elif reaction == 'sc':
    reactmulti = 1
    tdmg = lvmulti 
elif reaction == 'sht':
    reactmulti = 1
    tdmg = lvmulti * 3
emmultiA = 2.78 * ttlem / (ttlem + 1400) + 1
emmultiT = 16 * ttlem / (ttlem + 2000) + 1
defmulti = (100 + chrlv) / ((100 + chrlv) + (enemlv + 100) * (1 - defreduc))
resmultiA = resCalc(enemresA,resreducA)
resmultiT = resCalc(enemresT,resreducT)
resmultiP = resCalc(enemresP,resreducP)

# damage formula (E for elemental dmg, P for physical dmg. T stands for transformative reaction and A for amplifying)
avgEdmg = atkstt * critmulti * dmgmulti * reactmulti * emmultiA * defmulti * resmultiA + tdmg * emmultiT * resmultiT
avgPdmg = atkstt * critmulti * dmgmulti * defmulti * resmultiP

stop = timeit.default_timer()
print('Time: ', stop - start)
plt.show()
