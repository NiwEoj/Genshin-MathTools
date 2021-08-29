import matplotlib.pyplot as plt
import seaborn as sns
import random as rd
import timeit
import pandas as pd
sns.set_style("darkgrid")

start = timeit.default_timer()

# load character and weapon stats
wpnoptions = {'Name':['Rust','Slingshot','Blackcliff','Harp'],
              'BaseAtk':[510,354,565,674],
              'scdSttType':['Atk','Crt','Cdmg','Crt'],
              'scdStt':[.413,.312,.368,.221]}
artDB = {'Name':['glad','cw','shimenawa','hod','fate','bc','pf','no','wt','scholar','martial'],
         'Rarity':[5,5,5,5,5,5,5,5,5,4,4],
         'twopc':['Atk','Edmg','Atk','Edmg','ER','Pdmg','Pdmg','Burst','EM','ER','Atk'],
         'twopcelem':['n','pyro','n','hydro','n','n','n','n','n','n','n'],
         'twopcStt':[.18,.15,.18,.15,.2,.25,.25,.2,80,.2,.18],
         'fourpc':[('normal',),('reactbnsA','reactbnsT','Edmg'),('normal','charge','plunge'),('normal','charge'),('',),('charge',),('atk','Pdmg'),('',),('charge',),('',),('normal','charge')],
         'fourpcstacks':[(1,),(1,1,3),(1,1,1),(1,1),(1,),(1,),(2,1),(1,),(1,),(1,),(1,1)],
         'fourpcStt':[(.35,),(.15,.4,.075),(.5,.5,.5),(.3,.3),(None,),(.5,),(.09,.25),(None,),(.35,),(None,),(.25,.25)],
         'fourpcreactT':[(),('ov','burn'),(),(),(),(),(),(),(),(),()]}
charatk = 244
chardef = 594
charhp = 9189
ascatk,asccrit,ascem = (.24,0,0)
lvmulti = 725                         # base dmg at lv70, 80, 90 is 383, 540, 725
numOfWpn = len(wpnoptions['Name'])
reaction = 'ov'

# mv is motion value for elemental dmg, mvP is for physical; mv[0] is mv per second of normals, [3] and [4] is mv per second of charge and plunge. 
# [1] and [2] is total mv, not mv per second 
mv = (0,20.33,6.38,0,0)
mvP = (0,0,0,0,0)

# [0], [3] and [4] shows the time spent on doing the respective move. [1] and [2] shows the number of times the skill is used.
sklweight = (0,1,1,0,0)

# reactuptime is the percentage of damage that was able to do A-reactions; in the case of T-reactions, [0],[3] and [4] is the no. of
# reactions per unit time, but [1] and [2] is the number of reactions for the duration of the skill
reactuptime = (0,4,0,0,0)

# artifact quality
artiq = 3.622 

# graph subplots
rows, columns = (2,2)
fig,ax = plt.subplots(rows, columns)

# number of sims
N = 500

def artDef(artName,pcnum,stack=1,uptime=1):
    global ttlatkp,ttldmgbnsE,ttldmgbnsP,ttlreactbnsT,ttlreactbnsA,ttlem,ttler,ttlcrit
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
    if pcnum >= 4:
        for i in range(len(artDB['fourpc'][idx])):                          
            stacks = min(stack,artDB['fourpcstacks'][idx][i])
            if artDB['fourpc'][idx][i] == 'normal':
                ttldmgbnsE[0] = ttldmgbnsE[0] + artDB['fourpcStt'][idx][i] * uptime
                ttldmgbnsP[0] = ttldmgbnsP[0] + artDB['fourpcStt'][idx][i] * uptime
            elif artDB['fourpc'][idx][i] == 'burst':
                ttldmgbnsE[2] = ttldmgbnsE[2] + artDB['fourpcStt'][idx][i] * uptime
                ttldmgbnsP[2] = ttldmgbnsP[2] + artDB['fourpcStt'][idx][i] * uptime 
            elif artDB['fourpc'][idx][i] == 'charge':
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
                ttlcrit = ttlcrit + .2 * stacks
        if artName == 'fate':
            ttldmgbnsE[2] = ttldmgbnsE[2] + min(ttler * .25,.75)             

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

# Monte-carlo sim
hatk = [0]*numOfWpn
optcrit = [0]*numOfWpn
optcdmg = [0]*numOfWpn
optatk = [0]*numOfWpn
baseatk = [0]*numOfWpn
optdmgbns,optem = ([0]*numOfWpn,[0]*numOfWpn)
defmulti = 0.5
j = 0
k = 0

for n in range(numOfWpn):
    crit = [0]*N
    effatk = [0]*N
    wpnatk = wpnoptions['BaseAtk'][n]
    wpnatkp,wpncrit,wpncdmg,wpnem = (0,0,0,0)
    if wpnoptions['scdSttType'][n] == 'Atk':
        wpnatkp = wpnoptions['scdStt'][n]
    elif wpnoptions['scdSttType'][n] == 'Crt':
        wpncrit = wpnoptions['scdStt'][n]
    elif wpnoptions['scdSttType'][n] == 'Cdmg':
        wpncdmg = wpnoptions['scdStt'][n]
    elif wpnoptions['scdSttType'][n] == 'Em':
        wpnem = wpnoptions['scdStt'][n]
    ttlatkp = ascatk + wpnatkp
    ttlcrit = .05 + wpncrit + asccrit
    ttlcdmg = .5 + wpncdmg
    ttldmgbnsE = [0]*5
    ttldmgbnsP = [0]*5
    ttlem = wpnem + ascem
    ttlreactbnsA = 0
    ttlreactbnsT = 0
    baseatk[n] = charatk + wpnatk
    if (reaction == 'vape') or (reaction == 'melt'):
        for i in range(N):
            dmgbns = rd.randint(0,1) * .466
            rem = artiq - dmgbns/.75
            atk = 0.75*rd.uniform(.622,rem) 
            rem = rem - atk/.75
            em = rd.uniform(0,rem) * 300
            rem = rem - em/300
            emmultiA = 2.78 * (ttlem + em) / (ttlem + em + 1400) + ttlreactbnsA 
            emmultiT = 16 * (ttlem + em) / (ttlem + em + 2000) + ttlreactbnsT + 1
            crit[i] = (rem + ttlcdmg + 2*ttlcrit)/4 
            cdmg =  max(crit[i]*2 ,ttlcdmg)
            for m in range(len(ttldmgbnsE)):
                effatk[i] = effatk[i] + (1 + crit[i]*(cdmg)) * ((baseatk[n])*(1 + ttlatkp + atk)+311) * (ttldmgbnsE[m] + dmgbns + 1) * mv[m] * sklweight[m] * (1 + reactmulti * emmultiA * rAuptime[m]) * defmulti
                effatk[i] = effatk[i] + (1 + crit[i]*(cdmg)) * ((baseatk[n])*(1 + ttlatkp + atk)+311) * (ttldmgbnsP[m] + dmgbns + 1) * mvP[m] * sklweight[m] * defmulti
            if effatk[i] > hatk[n]:
                hatk[n] = effatk[i] 
                optcrit[n] = crit[i] 
                optcdmg[n] = cdmg 
                optatk[n] = atk + ascatk + 311/baseatk[n]
                optdmgbns[n] = dmgbns 
                optem[n] = ttlem + em
    elif (tdmg > 0):
        for i in range(N):
            dmgbns = rd.randint(0,1) * .466
            rem = artiq - dmgbns/.75
            atk = 0.75*rd.uniform(.622,rem) 
            rem = rem - atk/.75
            em = rd.uniform(0,rem) * 300
            rem = rem - em/300
            emmultiA = 2.78 * (ttlem + em) / (ttlem + em + 1400) + ttlreactbnsA 
            emmultiT = 16 * (ttlem + em) / (ttlem + em + 2000) + ttlreactbnsT + 1
            crit[i] = (rem + ttlcdmg + 2*ttlcrit)/4 
            cdmg =  max(crit[i]*2 ,ttlcdmg)
            for m in range(len(ttldmgbnsE)):
                effatk[i] = effatk[i] + (1 + crit[i]*(cdmg)) * ((baseatk[n])*(1 + ttlatkp + atk)+311) * (ttldmgbnsE[m] + dmgbns + 1) * mv[m] * sklweight[m] * defmulti 
                effatk[i] = effatk[i] + tdmg * emmultiT * rTuptime[m] 
                effatk[i] = effatk[i] + (1 + crit[i]*(cdmg)) * ((baseatk[n])*(1 + ttlatkp + atk)+311) * (ttldmgbnsP[m] + dmgbns + 1) * mvP[m] * sklweight[m] * defmulti
            if effatk[i] > hatk[n]:
                hatk[n] = effatk[i] 
                optcrit[n] = crit[i] 
                optcdmg[n] = cdmg 
                optatk[n] = atk + ascatk + 311/baseatk[n]
                optdmgbns[n] = dmgbns 
                optem[n] = ttlem + em
    else:
        for i in range(N):
            dmgbns = rd.randint(0,1) * .466
            rem = artiq - dmgbns/.75
            atk = 0.75*rd.uniform(.622,rem) 
            rem = rem - atk/.75
            crit[i] = (rem + ttlcdmg + 2*ttlcrit)/4 
            cdmg =  max(crit[i]*2 ,ttlcdmg)
            for m in range(len(ttldmgbnsE)):
                effatk[i] = effatk[i] + (1 + crit[i]*(cdmg)) * ((baseatk[n])*(1 + ttlatkp + atk)+311) * (ttldmgbnsE[m] + dmgbns + 1) * mv[m] * sklweight[m] * defmulti
                effatk[i] = effatk[i] + (1 + crit[i]*(cdmg)) * ((baseatk[n])*(1 + ttlatkp + atk)+311) * (ttldmgbnsP[m] + dmgbns + 1) * mvP[m] * sklweight[m] * defmulti
            if effatk[i] > hatk[n]:
                hatk[n] = effatk[i] 
                optcrit[n] = crit[i] 
                optcdmg[n] = cdmg 
                optatk[n] = atk + ascatk + 311/baseatk[n]
                optdmgbns[n] = dmgbns 
                optem[n] = ttlem 

    # plot graph
    ax[j,k].scatter(crit,effatk)
    ax[j,k].set_title(wpnoptions['Name'][n])
    ax[j,k].set_xlabel('Crit rate')
    ax[j,k].set_ylabel('Effective attack')
    if k == columns-1:
        j = j + 1
        k = 0
    else:
        k = k + 1

# print additional info
print("Best performing weapon is",wpnoptions['Name'][hatk.index(max(hatk))])
dic = {'Name':[],'Optimum Attack':[],'Optimum Crit Rate':[],'Optimum Crit Dmg':[],'Optimum Dmg Bns':[],'Optimal EM':[]}
for n in range(numOfWpn):
    dic['Name'] = dic['Name'] + [wpnoptions['Name'][n]]
    dic['Optimum Attack'] = dic['Optimum Attack'] + [round((optatk[n] + 1)*baseatk[n])]
    dic['Optimum Crit Rate'] = dic['Optimum Crit Rate'] + [str(round(optcrit[n]*100,1)) + "%"]
    dic['Optimum Crit Dmg'] = dic['Optimum Crit Dmg'] + [str(round(optcdmg[n]*100,1)) + "%"]
    dic['Optimum Dmg Bns'] = dic['Optimum Dmg Bns'] + [str(round(optdmgbns[n]*100,1)) + "%"]
    dic['Optimal EM'] = dic['Optimal EM'] + [str(round(optem[n]))]
print(pd.DataFrame(dic))

stop = timeit.default_timer()
print('Time: ', stop - start)
plt.show()
