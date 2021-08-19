from collections import Counter

chrelem,chrwpn = ('pyro','gs')
reaction = 'vape'
ttlatkp = 2.2
ttldmgbnsE = [1,1,1,1,1]
ttldmgbnsP = [1,1,1,1,1]
ttlreactbnsA = 0
ttlreactbnsT = 0
arttype = ['glad','glad','cw','cw','cw']
artstack = 3        # how to add this into user interface?


def artBns(x,y):
    global ttlatkp,ttldmgbnsE,ttldmgbnsP,ttlreactbnsT,ttlreactbnsA
    if x == 'glad':
        ttlatkp = ttlatkp + .18
        if y == 4:
            if (chrwpn == 'pol') or (chrwpn == 'swd') or (chrwpn == 'gs'):
                ttldmgbnsE[0] = ttldmgbnsE[0] + .35
                ttldmgbnsP[0] = ttldmgbnsP[0] + .35
    elif x == 'cw':
        if chrelem == 'pyro':
            if y == 2:
                artstack = 0
            if y == 4:
                ttlreactbnsA = ttlreactbnsA + .15
                ttlreactbnsT = ttlreactbnsT + .4
            for i in range(len(ttldmgbnsE)):
                ttldmgbnsE[i] = ttldmgbnsE[i] + .075*(artstack + 2)
        elif (reaction == 'ov') and (y == 4):
            ttlreactbnsT = ttlreactbnsT + .4


a = Counter(arttype)
b = a.most_common(2)
if b[0][1] > 3:
    artBns(b[0][0],4)
elif b[0][1] > 1:
    artBns(b[0][0],2)
    if b[1][1] > 1:
        artBns(b[1][0],2)

