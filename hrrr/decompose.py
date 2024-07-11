import numpy as np

# identify proper aggregation sizes and configurations

#### USER INPUT ####
base_ewe=150
base_esn=150

min_ewe=80
max_ewe=300
min_esn=80
max_esn=300

minp=12
maxp=15

dx=3 #km

TSmax=250#maximum tile size
minopts=3

minTS=55 #minimum, maximum TS required to report

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
            if (len(TSs)>=minopts):
                if (np.max(TSs)<minTS):
                    continue
                print('POSSIBLE TS/n combos for '+str(e_we)+' and '+str(e_sn)+'  :: '+str(e_we*e_sn/prcs/1000))
                for TS in TSs[-1:]:
                    print('    Ts: '+str(TS)+'  n: '+str(prcs))
