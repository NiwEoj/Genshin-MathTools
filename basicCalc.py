import matplotlib.pyplot as plt
from numpy import empty
import seaborn as sns
import random as rd
import timeit
import pandas as pd
from collections import Counter
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

# uptime = (period of time when passive is up) / (period of time for a rotation)
def artDef(artName,pcnum,stack=1,uptime=1):
    global ttlatkp,ttldmgbnsE,ttldmgbnsP,ttlreactbnsT,ttlreactbnsA,ttlem,ttler,ttlcrit,ttlhpp
    idx = artDB['Name'].index(artName)
    if artDB['twopc'][idx] == 'Atk':
        ttlatkp = ttlatkp + artDB['twopcStt'][idx]
    elif artDB['twopc'][idx] == 'Pdmg':
        for i in range(len(ttldmgbnsP)):
            ttldmgbnsP[i] = ttldmgbnsP[i] + artDB['twopcStt'][idx]
    elif (artDB['twopc'][idx] == 'Edmg') and (artDB['twopcelem'][idx] == chrelem):
        for i in range(len(ttldmgbnsE)):
            ttldmgbnsE[i] = ttldmgbnsE[i] + artDB['twopcStt'][idx]
    elif artDB['twopc'][idx] == 'Burst':
        ttldmgbnsE[2] = ttldmgbnsE[2] + artDB['twopcStt'][idx]
    elif artDB['twopc'][idx] == 'EM':
        ttlem = ttlem + artDB['twopcStt'][idx]
    elif artDB['twopc'] == 'ER':
        ttler = ttler + artDB['twopcStt'][idx]
    elif artDB['twopc'] == 'HP':
        ttlhpp = ttlhpp + artDB['twopcStt'][idx]
    if pcnum >= 4:
        for i in range(len(artDB['fourpc'][idx])):                          
            stacks = min(stack,artDB['fourpcstacks'][idx][i])
            if artDB['fourpc'][idx][i] == 'normal':
                if (artName!='glad'):
                    ttldmgbnsE[0] = ttldmgbnsE[0] + artDB['fourpcStt'][idx][i] * uptime
                    ttldmgbnsP[0] = ttldmgbnsP[0] + artDB['fourpcStt'][idx][i] * uptime
                elif (chrwpn=='sword') or (chrwpn=='claymore') or (chrwpn=='polearm'):
                    ttldmgbnsE[0] = ttldmgbnsE[0] + artDB['fourpcStt'][idx][i] * uptime
                    ttldmgbnsP[0] = ttldmgbnsP[0] + artDB['fourpcStt'][idx][i] * uptime
            elif artDB['fourpc'][idx][i] == 'burst':
                ttldmgbnsE[2] = ttldmgbnsE[2] + artDB['fourpcStt'][idx][i] * uptime
                ttldmgbnsP[2] = ttldmgbnsP[2] + artDB['fourpcStt'][idx][i] * uptime 
            elif artDB['fourpc'][idx][i] == 'charge':
                if (artName!='wt'):
                    ttldmgbnsE[3] = ttldmgbnsE[3] + artDB['fourpcStt'][idx][i] * uptime 
                    ttldmgbnsP[3] = ttldmgbnsP[3] + artDB['fourpcStt'][idx][i] * uptime 
                elif (chrwpn=='bow') or (chrwpn=='catalyst'):
                    ttldmgbnsE[3] = ttldmgbnsE[3] + artDB['fourpcStt'][idx][i] * uptime 
                    ttldmgbnsP[3] = ttldmgbnsP[3] + artDB['fourpcStt'][idx][i] * uptime 
            elif artDB['fourpc'][idx][i] == 'plunge':
                ttldmgbnsE[4] = ttldmgbnsE[4] + artDB['fourpcStt'][idx][i] * uptime 
                ttldmgbnsP[4] = ttldmgbnsP[4] + artDB['fourpcStt'][idx][i] * uptime 
            elif artDB['fourpc'][idx][i] == 'reactbnsA': 
                ttlreactbnsA = ttlreactbnsA + artDB['fourpcStt'][idx][i] * uptime 
            elif artDB['fourpc'][idx][i] == 'reactbnsT':
                if reaction in artDB['fourpcreactT'][idx]:
                    ttlreactbnsT = ttlreactbnsT + artDB['fourpcStt'][idx][i] * uptime 
            elif artDB['fourpc'][idx][i] == 'Edmg':
                for j in range(len(ttldmgbnsE)):
                    ttldmgbnsE[j] = ttldmgbnsE[j] + artDB['fourpcStt'][idx][i] * stacks * uptime
            elif artDB['fourpc'][idx][i] == 'Pdmg':
                if ((artName == 'pf') and (stack == 2)) or (artName != 'pf'):
                    for j in range(len(ttldmgbnsP)):
                        ttldmgbnsP[j] = ttldmgbnsP[j] + artDB['fourpcStt'][idx][i] * uptime 
            elif artDB['fourpc'][idx][i] == 'atk':
                ttlatkp = ttlatkp + artDB['fourpcStt'][idx][i] * stacks * uptime
            elif artDB['fourpc'][idx][i] == 'crit':
                ttlcrit = ttlcrit + artDB['fourpcStt'][idx][i] * stacks * uptime
        if artName == 'fate':
            ttldmgbnsE[2] = ttldmgbnsE[2] + min(ttler * .25,.75)             

# load base info/stats 
reaction = 'ec'
lvmulti = 725                         # base transformative dmg. Base dmg at lv70, 80, 90 is 383, 540, 725
chrlv,chratk,chrdef,chrhp,chrelem,chrwpn = (90,244,594,9189,'electro','bow')
asccrit,asccdmg,ascatk,ascem,ascdef,aschp,ascdmgbns,ascpdmgbns = (0,0,.24,0,0,0,0,0)
wpnatk,wpncrit,wpncdmg,wpnatkp,wpnem,wpndef,wpnhp = (510,0,0,.413,0,0,0)        # wpnatk is weapon base atk stat, wpnatkp is its secondary stat if it has atk as secondary
wpnpdmgbns = 0
artcrit,artcdmg,artatk,artatkflat,artem,artdef,artdefflat,arthp,arthpflat,artdmgbns = (.55,.7,.7,0,0,0,0,0,0,.466)
artpdmgbns = 0
artflower,artfeather = (4780,311)
artreactbnsA,artreactbnsT = (0,0)
arttype = ['glad','glad','cw','cw','cw']
artstack = 1
resreducA,resreducT,resreducP = (0,0,0)
defreduc = 0
enemlv = 90
enemresA,enemresT,enemresP = (.1,.1,.1)
artDB = {'Name':['glad','cw','shimenawa','hod','fate','bc','pf','no','wt','scholar','martial'],
         'Rarity':[5,5,5,5,5,5,5,5,5,4,4],
         'twopc':['Atk','Edmg','Atk','Edmg','ER','Pdmg','Pdmg','Burst','EM','ER','Atk'],
         'twopcelem':['n','pyro','n','hydro','n','n','n','n','n','n','n'],
         'twopcStt':[.18,.15,.18,.15,.2,.25,.25,.2,80,.2,.18],
         'fourpc':[('normal',),('reactbnsA','reactbnsT','Edmg'),('normal','charge','plunge'),('normal','charge'),('',),('charge',),('atk','Pdmg'),('',),('charge',),('',),('normal','charge')],
         'fourpcstacks':[(1,),(1,1,3),(1,1,1),(1,1),(1,),(1,),(2,1),(1,),(1,),(1,),(1,1)],
         'fourpcStt':[(.35,),(.15,.4,.075),(.5,.5,.5),(.3,.3),(None,),(.5,),(.09,.25),(None,),(.35,),(None,),(.25,.25)],
         'fourpcreactT':[(),('ov','burn'),(),(),(),(),(),(),(),(),()]}

# reactuptime is the percentage of damage that was able to do A-reactions; in the case of T-reactions, [0],[3] and [4] is the no. of
# reactions per unit time, but [1] and [2] is the number of reactions for the duration of the skill
reactuptime = (0.5,5,1,0,0)

# mv is motion value for elemental dmg, mvP is for physical; mv[0] is mv per second of normals, [3] and [4] is mv per second of charge and plunge. 
# [1] and [2] is total mv, not mv per second 
mv = (.7,20,2,0,0)
mvP = (2,0,0,0,0)

# [0], [3] and [4] shows the time spent on doing the respective move. [1] and [2] shows the number of times the skill is used.
sklweight = (0,0,0,0,0)

# adding up stats for later use 
baseatk = wpnatk + chratk
ttlatkp = ascatk + artatk + wpnatkp + 1
ttlcrit = .05 + asccrit + wpncrit + artcrit
ttlcdmg = .5 + asccdmg + wpncdmg + artcdmg
ttlem = ascem + wpnem +  artem
ttlhpp = aschp + arthp + wpnhp + 1
ttldefp = ascdef + artdef + wpndef + 1
ttldmgbnsE = artdmgbns + ascdmgbns + 1
ttldmgbnsE = [ttldmgbnsE]*5
ttldmgbnsP = artpdmgbns + wpnpdmgbns + ascpdmgbns + 1
ttldmgbnsP = [ttldmgbnsP]*5
ttlreactbnsA = 0
ttlreactbnsT = 0
A,B,C,D,E,F,G,H = (ttlatkp,tuple(ttldmgbnsE),tuple(ttldmgbnsP),ttlreactbnsT,ttlreactbnsA,ttlem,ttler,ttlcrit)
if reaction == 'vape':
    reactmulti = 1.5 
    tdmg = 0 
    rAuptime = reactuptime
elif reaction =='melt':
    reactmulti = 2 
    tdmg = 0
    rAuptime = reactuptime
elif reaction == 'swl':
    reactmulti = 1
    tdmg = lvmulti * 1.2
    rTuptime = reactuptime
elif reaction == 'ov':
    reactmulti = 1
    tdmg = lvmulti * 4
    rTuptime = reactuptime
elif reaction == 'ec':
    reactmulti = 1
    tdmg = lvmulti * 4.8
    rTuptime = reactuptime
elif reaction == 'sc':
    reactmulti = 1
    tdmg = lvmulti 
    rTuptime = reactuptime
elif reaction == 'sht':
    reactmulti = 1
    tdmg = lvmulti * 3
    rTuptime = reactuptime
else:
    reactmulti = 1
    tdmg = 0

# artifact passives
artCount = Counter(arttype)
b = artCount.most_common(2)
if b[0][1] > 1:
    artDef(b[0][0],b[0][1])
if b[1][1] > 1:
    artDef(b[1][0],b[1][1])

# weapon passives


# multiplying the stats prepared above
ttlhp = chrhp * ttlhpp + artflower + arthpflat
ttldef = chrdef * ttldefp + artdefflat
ttlatk = baseatk * ttlatkp + artfeather + artatkflat
critmulti = 1 + ttlcrit * ttlcdmg
emmultiA = 2.78 * ttlem / (ttlem + 1400) + ttlreactbnsA 
emmultiT = 16 * ttlem / (ttlem + 2000) + ttlreactbnsT + 1
defmulti = (100 + chrlv) / ((100 + chrlv) + (enemlv + 100) * (1 - defreduc))
resmultiA = resCalc(enemresA,resreducA)
resmultiT = resCalc(enemresT,resreducT)
resmultiP = resCalc(enemresP,resreducP)


# damage formula (E for elemental dmg, P for physical dmg. T stands for transformative reaction and A for amplifying)
# avgEdmg etc is consists of 3 sources; avgEdmg[0] = Normals, [1] = E.Skill, [2] = E.Burst, [3] = Charge atk, [4] = Plunge atk
avgEdmg,avgReactiondmg,avgPdmg = ([0]*5,[0]*5,[0]*5)
if tdmg == 0:  
    if reactmulti == 1:
        for i in range(len(avgEdmg)):
            avgEdmg[i] = ttlatk * critmulti * ttldmgbnsE[i] * defmulti * resmultiA * mv[i]
            avgReactiondmg[i] = 0
            avgPdmg[i] = ttlatk * critmulti * ttldmgbnsP[i] * defmulti * resmultiP * mvP[i]
    else:
        for i in range(len(avgEdmg)):
            avgEdmg[i] = ttlatk * critmulti * ttldmgbnsE[i] * defmulti * resmultiA * mv[i]
            avgReactiondmg[i] = avgEdmg[i] * reactmulti * emmultiA * rAuptime[i]
            avgPdmg[i] = ttlatk * critmulti * ttldmgbnsP[i] * defmulti * resmultiP * mvP[i]
else:
    for i in range(len(avgEdmg)):
        avgEdmg[i] = ttlatk * critmulti * ttldmgbnsE[i] * defmulti * resmultiA * mv[i]
        avgReactiondmg[i] = tdmg * emmultiT * resmultiT * rTuptime[i] 
        avgPdmg[i] = ttlatk * critmulti * ttldmgbnsP[i] * defmulti * resmultiP * mvP[i]

# construct dataframe 
df = pd.DataFrame()
df['Damage Source'] = ['Normals','Elemental Skill','Elemental Burst','Charge Attack','Plunge Attack']
df['Elemental Damage'] = avgEdmg
df['Reaction Damage'] = avgReactiondmg
df['Physical Damage'] = avgPdmg
print(df) 

# plot bar chart
plt.bar(df['Damage Source'],df['Elemental Damage'],color='red',label='Elemental Damage')
plt.bar(df['Damage Source'],df['Reaction Damage'],bottom=df['Elemental Damage'],color='orange',label='Reaction Damage')
plt.bar(df['Damage Source'],df['Physical Damage'],bottom=df['Elemental Damage']+df['Reaction Damage'],color='blue',label='Physical Damage')
plt.legend()

stop = timeit.default_timer()
print('Time: ', stop - start)
plt.show()
