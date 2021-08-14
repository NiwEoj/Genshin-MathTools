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
              'scdAtk':[.413,0,0,0],
              'scdCrt':[0,.312,0,.221],
              'scdCdmg':[0,0,.368,0]}
charatk = 244
chardef = 594
charhp = 9189
ascatk = 0.24
asccrit = 0
numOfWpn = len(wpnoptions['Name'])

# artifact quality
artiq = 3 

# graph subplots
rows, columns = (2,2)
fig,ax = plt.subplots(rows, columns)

# number of sims
N = 500

# Monte-carlo sim
hatk = [0]*numOfWpn
optcrit = [0]*numOfWpn
optcdmg = [0]*numOfWpn
optatk = [0]*numOfWpn
baseatk = [0]*numOfWpn
j = 0
k = 0

for n in range(numOfWpn):
    effatk = [0]*N
    crit = [0]*N
    wpnatk = wpnoptions['BaseAtk'][n]
    wpnatkp = wpnoptions['scdAtk'][n]
    wpncrit = wpnoptions['scdCrt'][n]
    wpncdmg = wpnoptions['scdCdmg'][n]
    ttlatkp = ascatk + wpnatkp
    ttlcrit = .05 + wpncrit + asccrit
    ttlcdmg = .5 + wpncdmg
    baseatk[n] = charatk + wpnatk
    for i in range(N):
        atk = 0.75*rd.uniform(.622,artiq) 
        rem = artiq - atk/.75 
        crit[i] = (rem + ttlcdmg + 2*ttlcrit)/4 
        cdmg =  crit[i]*2 
        effatk[i] = (1 + crit[i]*(cdmg))*((baseatk[n])*(1 + ttlatkp + atk)+311)  
        if effatk[i] > hatk[n]:
            hatk[n] = effatk[i] 
            optcrit[n] = crit[i] 
            optcdmg[n] = cdmg 
            optatk[n] = atk + ascatk + 311/baseatk[n]
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
dic = {'Name':[],'Optimum Attack':[],'Optimum Crit Rate':[],'Optimum Crit Dmg':[]}
for n in range(numOfWpn):
    dic['Name'] = dic['Name'] + [wpnoptions['Name'][n]]
    dic['Optimum Attack'] = dic['Optimum Attack'] + [round((optatk[n] + 1)*baseatk[n])]
    dic['Optimum Crit Rate'] = dic['Optimum Crit Rate'] + [str(round(optcrit[n]*100,1)) + "%"]
    dic['Optimum Crit Dmg'] = dic['Optimum Crit Dmg'] + [str(round(optcdmg[n]*100,1)) + "%"]
print(pd.DataFrame(dic))

stop = timeit.default_timer()
print('Time: ', stop - start)
plt.show()
