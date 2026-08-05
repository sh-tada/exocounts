from exocounts import exocounts
from exocounts import convmag

from astropy import units as u
from astropy import constants as const

import matplotlib.pyplot as plt
import pylab
import numpy as np

from ejas import current_jasmine


ejas, target, obs, Hw = current_jasmine()

shot=[]
dark=[]
read=[]
H=[]
J=[]
Hw=[]
darr=np.linspace(5,35,91)
magdict=convmag.get_magdict()
for distpc in darr:
    target.d=distpc*u.pc #change targets
    obs.target = target
    obs.update()
    Htmp = convmag.get_mag("H", obs.flux, magdict)
    Jtmp = convmag.get_mag("J", obs.flux, magdict)
    Hwtmp = 0.9 * Jtmp + 0.1 * Htmp - 0.06 * (Jtmp - Htmp)**2
    H.append(Htmp)
    J.append(Jtmp)
    Hw.append(Hwtmp)
    #print(distpc,convmag.get_mag("H",obs.flux,magdict))
    if obs.sat:
        satmag=[Hwtmp,Htmp,Jtmp]
    dark.append(obs.sigd_relative)
    read.append(obs.sigr_relative)
    shot.append(obs.sign_relative)
    
sigsarr_relative=np.array(shot)
sigdarr_relative=np.array(dark)
sigrarr_relative=np.array(read)
magarr=np.array(Hw)

fig=plt.figure(figsize=(7,5))

ax=fig.add_subplot(211)
ax.plot(magarr,sigsarr_relative,label="shot noise")
ax.plot(magarr,sigdarr_relative,label="dark noise",ls="dotted")
ax.plot(magarr,sigrarr_relative,label="read noise",ls="dashed")
pylab.legend()
pylab.xlim(7.5,11.2)
pylab.ylim(0,600)
#ax.fill([10,satmag[0],satmag[0],10.0,10.0],[0,0,600,600,0],alpha=0.3,color="gray")
for i,dpc in enumerate(darr):
    if np.mod(dpc,5)==0:
        plt.axvline(magarr[i],ls="dashed",color="gray",alpha=0.3)
plt.ylabel("noise for 5 min (ppm)")
ppm=1.e6

ax=fig.add_subplot(212)
ax.plot(magarr,np.sqrt(sigsarr_relative**2 + sigdarr_relative**2 + sigrarr_relative**2)/ppm*7*100)
pylab.xlim(7.5,11.2)
pylab.ylim(0,0.5)
a = 7.5
ax.fill([a,satmag[0],satmag[0],a,a],[0,0,1,1,0],alpha=0.3,color="gray")
plt.axhline(0.30,color="gray",alpha=0.2,c="orange")

for i,dpc in enumerate(darr):
    if np.mod(dpc,5)==0 and dpc>=10:
        plt.axvline(magarr[i],ls="dashed",color="gray",alpha=0.3)
        plt.text(magarr[i],0.05,str(int(dpc))+"pc",horizontalalignment="center")
plt.xlabel("Hw-band magnitude")
plt.ylabel("depth for 7 sigma \n limit in 5 min [%]")
plt.savefig("noise.png")
plt.savefig("noise.pdf", bbox_inches="tight", pad_inches=0.0)
plt.show()
