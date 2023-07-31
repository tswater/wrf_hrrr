import numpy as np

#### USER INPUT ####
base_ewe=1760
base_esn=1020

min_ewe=1500
max_ewe=1598
min_esn=1000
max_esn=1058

minp=5*32
maxp=7*32

dx=3 #km

TSmax=200#maximum tile size
minopts=4


#### DECOMP ####
def decomp(n):
    fc=factors(n)
    fc=list(fc)
    fo1=1
    fo2=n
    mindif=fo2-fo1
    for f in fc:
        for f2 in fc:
            if (f==f2)&(f==np.sqrt(n)):
                return f,f2
            if (fo2<fo1):
                continue
            if (fo2-fo1)<mindif:
                mindif=fo2-fo1
                fo1=f
                fo2=f2
    return fo1,fo2


from functools import reduce

def factors(n):    
    return set(reduce(list.__add__,([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))



#### CODE ####
for e_we in range(min_ewe,max_ewe+1,2):
    for e_sn in range(min_esn,max_esn+1,2):
        for prcs in range(minp,maxp+1):
            TSs=[]
            dc_we,dc_sn=decomp(prcs)
            for TS in range(6,TSmax,dx):    
                a_we=e_we/dc_we*dx/TS
                a_sn=e_sn/dc_sn*dx/TS
                if (int(a_we)==a_we) & (int(a_sn)==a_sn):
                    TSs.append(TS)
            if len(TSs)>=minopts:
                print('POSSIBLE TS/n combos for '+str(e_we)+' and '+str(e_sn))
                for TS in TSs:
                    print('    Ts: '+str(TS)+'  n: '+str(prcs))
