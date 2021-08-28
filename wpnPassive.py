chrelem,chrwpn = ('pyro','gs')
reaction = 'vape'
ttlatkp = 2.2
ttlcrit = .5
ttlem = 0
ttler = 1
ttldmgbnsE = [1,1,1,1,1]
ttldmgbnsP = [1,1,1,1,1]
ttlreactbnsA = 0
ttlreactbnsT = 0
wpnDB = {'Name':['Archaic','WGS','Serpent','Lithic'],
         'Basetk':[565,608,510,510],
         'scdSttType':['Atk','Atk','Crit','Atk'],
         'scdStt':[.276,.496,.276,.413],
         'psvType':[('crush',),('atk','atk'),('dmg',),('atk','crit')],
         'psvStt':[((2.4,3.0,3.6,4.2,4.8),),((.2,.25,.3,.35,.4),(.4,.5,.6,.7,.8)),((.06,.07,.08,.09,.1),),\
                   ((.07,.08,.09,.1,.11),(.03,.04,.05,.06,.07))],
         'psvStacks':[(1,),(1,1),(5,),(4,)]
        }

def wpnDef(wpnName,wpnRefine=1,wpnStack=1):
    global ttldmgbnsP,ttlatkp,ttlcrit,ttldmgbnsE,ttlem,ttler,ttlreactbnsA,ttlreactbnsT
    idx = wpnDB['Name'].index(wpnName)
    for i in range(len(wpnDB['psvType'][idx])):
        stacks = min(wpnStack,wpnDB['psvStacks'][idx][i])
        if wpnDB['psvType'][idx][i] == 'atk':
            ttlatkp = ttlatkp + wpnDB['psvStt'][idx][i][wpnRefine-1] * stacks
        elif wpnDB['psvType'][idx][i] == 'crit':
            ttlcrit = ttlcrit + wpnDB['psvStt'][idx][i][wpnRefine-1] * stacks
        elif wpnDB['psvType'][idx][i] == 'dmg':
            for j in range(len(ttldmgbnsE)):
                ttldmgbnsE[j] = ttldmgbnsE[j] + wpnDB['psvStt'][idx][i][wpnRefine-1] * stacks
                ttldmgbnsP[j] = ttldmgbnsP[j] + wpnDB['psvStt'][idx][i][wpnRefine-1] * stacks
        elif wpnDB['psvType'][idx][i] == 'cdmg':
            ttlcdmg = ttlcdmg + wpnDB['psvStt'][idx][i][wpnRefine-1] * stacks
        
        
