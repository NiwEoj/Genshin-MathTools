from collections import Counter

chrelem,chrwpn = ('pyro','gs')
reaction = 'vape'
ttlatkp = 2.2
ttlem = 0
ttler = 1
ttldmgbnsE = [1,1,1,1,1]
ttldmgbnsP = [1,1,1,1,1]
ttlreactbnsA = 0
ttlreactbnsT = 0
arttype = ['glad','glad','cw','cw','cw']
artstack = 3        # how to add this into user interface?
artDB = {'Name':['glad','cw','shimenawa','hod','fate','bc','pf','no','wt','scholar','martial'],
         'Rarity':[5,5,5,5,5,5,5,5,5,4,4],
         'twopc':['Atk','Edmg','Atk','Edmg','ER','Pdmg','Pdmg','Burst','EM','ER','Atk'],
         'twopcelem':['n','pyro','n','hydro','n','n','n','n','n','n','n'],
         'twopcStt':[.18,.15,.18,.15,.2,.25,.25,.2,80,.2,.18],
         'fourpc':[('normal'),('reactbnsA','reactbnsT','Edmg'),('normal','charge','plunge'),('normal','charge'),('burst'),('charge'),('atk','Pdmg'),(''),('charge'),(''),('normal','charge')],
         'fourpcstacks':[(1),(1,1,3),(1,1,1),(1,1),(1),(1),(2,1),(1),(1),(1),(1,1)],
         'fourpcStt':[(.35),(.15,.4,.075),(.5,.5,.5),(.3,.3),(),(.5),(.09,.25),(),(.35),(),(.25,.25)],
         'fourpcreactT':[(),('ov','burn'),(),(),(),(),(),(),(),(),()]}

def artDef(artName,pcnum,stack=1,uptime=1):
    global ttlatkp,ttldmgbnsE,ttldmgbnsP,ttlreactbnsT,ttlreactbnsA,ttlem,ttler
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
                for j in range(len(ttldmgbnsP)):
                    ttldmgbnsP[j] = ttldmgbnsP[j] + artDB['fourpcStt'][idx][i] * uptime 
            elif artDB['fourpc'][idx][i] == 'atk':
                if ((artName == 'pf') and (stacks != 2)) or (artName != 'pf'):
                    ttlatkp = ttlatkp + artDB['fourpcStt'][idx][i] * uptime
        if artName == 'fate':
            fatebns = min(ttler*.25,.75)
            ttldmgbnsE[2] = ttldmgbnsE[2] + fatebns                    

artCount = Counter(arttype)
b = artCount.most_common(2)
if b[0][1] > 1:
    artDef(b[0][0],b[0][1])
if b[1][1] > 1:
    artDef(b[1][0],b[1][1])

print('ttlatkp: ',ttlatkp)
print('ttldmgbnsE',ttldmgbnsE)
print('ttlreactbnsA: ',ttlreactbnsA)
print('ttlreactbnsT',ttlreactbnsT)

