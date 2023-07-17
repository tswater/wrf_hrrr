import os
import subprocess as sp

error_dir='logs/'

for file in os.listdir(error_dir):
    if 'rsl.error' in file:
        fp=open(error_dir+file,'r',errors='ignore')
        for line in fp.readlines():
            if ('FATAL' in line) or ('Fortran runtime error' in line):
                print('ERROR FOUND in '+file)
                sp.run('tail -n 5 '+file,shell=True)
                print()
                print()
                break
