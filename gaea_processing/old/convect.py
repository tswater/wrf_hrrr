import numpy as np
import os
from subprocess import run
import netCDF4 as nc

gaea_dir='/home/tsw35/xTyc_shared/compressed_output/'
odir='/home/tsw35/tyche/wrf_gaea/'

# find all days
days=[]
for day in os.listdir(gaea_dir):
    if 'het' in day:
        continue
    day_=day[0:8]
    n1=len(os.listdir(gaea_dir+day_+'_het'))
    n2=len(os.listdir(gaea_dir+day_+'_hmg'))
    if (n1<48) or (n2<48):
        continue

    days.append(day_)


def vari(data,df=20):
    ni=data.shape[0]
    nj=data.shape[1]
    dout=np.zeros((ni,nj))
    for i in range(int((ni+1)/df)):
        for j in range(int((nj+1)/df)):
            dout[i*df:(i+1)*df,j*df:(j+1)*df] = np.nanvar(data[i*df:(i+1)*df,j*df:(j+1)*df])
    return dout

def meani(data,df=20):
    ni=data.shape[0]
    nj=data.shape[1]
    dout=np.zeros((ni,nj))
    for i in range(int((ni+1)/df)):
        for j in range(int((nj+1)/df)):
            dout[i*df:(i+1)*df,j*df:(j+1)*df] = np.nanmean(data[i*df:(i+1)*df,j*df:(j+1)*df])
    return dout



N=49

days.sort()

for day in days:
    print(day)
    hrs=os.listdir(gaea_dir+day+'_het/')
    hrs.sort()

    #fphet0=nc.Dataset(gaea_dir+day+'_het/'+hrs[24],'r')
    het_r=np.zeros((N,1039,1559))
    het_h=np.zeros((N,1039,1559))
    het_h60=np.zeros((N,1039,1559))
    het_vh=np.zeros((N,1039,1559))
    hmg_h=np.zeros((N,1039,1559))
    hmg_r=np.zeros((N,1039,1559))
    
    i=0
    for hr in hrs:
        print(hr)
        fphet=nc.Dataset(gaea_dir+day+'_het/'+hr,'r')
        fphmg=nc.Dataset(gaea_dir+day+'_hmg/'+hr,'r')
        
        het_r[i,:,:]=fphet['RAINNC'][0,:,:]
        hmg_r[i,:,:]=fphmg['RAINNC'][0,:,:]

        het_h[i,:,:]=fphet['HFX'][0,:,:]
        hmg_h[i,:,:]=fphmg['HFX'][0,:,:]

        het_vh[i,:,:]=vari(het_h[i,:,:])
        het_h[i,:,:]=meani(het_h[i,:,:])
        
        i=i+1
    try:
        fp=nc.Dataset(odir+day+'_conv.nc','r+')
    except Exception:
        fp=nc.Dataset(odir+day+'_conv.nc','w')
        fp.createDimension('we',1559)
        fp.createDimension('sn',1039)
        fp.createDimension('time',N)
    

    # OUTPUT info
    try:
        fp.createVariable('time','i4',('time'))
        fp['time'][:]=list(range(49))
    except:
        pass

    try:
        fp.createVariable('RAINNC_het','f4',('time','sn', 'we'))
    except Exception:
        pass
    try:
        fp.createVariable('RAINNC_hmg','f4',('time','sn', 'we'))
    except Exception:
        pass
    try:
        fp.createVariable('HFX_het','f4',('time','sn', 'we'))
    except Exception:
        pass
    try:
        fp.createVariable('HFX_hmg','f4',('time','sn', 'we'))
    except Exception:
        pass
    try:
        fp.createVariable('HFX_het60','f4',('time','sn', 'we'))
    except Exception:
        pass
    try:
        fp.createVariable('HFX_hetvar','f4',('time','sn', 'we'))
    except Exception:
        pass


    fp['RAINNC_het'][:]=het_r[:]
    fp['RAINNC_hmg'][:]=hmg_r[:]
    
    fp['HFX_het'][:]=het_h[:]
    fp['HFX_hmg'][:]=hmg_h[:]

    fp['HFX_het60'][:]=het_h60[:]
    fp['HFX_hetvar'][:]=het_vh[:]

    fp.close()


