# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 14:47:36 2025

@author: nicol
"""
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib import cm
import copy as cp
import numpy as np
import xarray as xr
import os
import cftime
import datetime as dt
from dateutil import parser

methods = ['ssrd_str',
          'ssr_str',
          'clark',
          'ssr_clark',
          'hastenrath_lamb',
          'ssr_hastenrath_lamb',
          'berliand_berliand',
          'ssr_berliand_berliand',
          'josey2',
          'ssr_josey2',
          'josey1',
          'ssr_josey1',
          'cal_str',
          'ssr_strd',
          'ssrd_strd',
          'bignami',
          'ssr_bignami',
          ]
method_names =  ['ssrd & str',
                 'ssr & str',
                 'calc. & Clark',
                 'ssr & Clark',
                 'calc. & Hast. & Lamb',
                 'ssr & Hast. & Lamb',
                 'calc. & Berl. & Berl.',
                 'ssr & Berl. & Berl.',
                 'calc. & Josey 2',
                 'ssr & Josey 2',
                 'calc. & Josey 1',
                 'ssr & Josey 1',
                 'calc. & str',
                 'ssr & strd',
                 'ssrd & strd',
                 'calc. & Bignami',
                 'ssr & Bignami',
                 ]

plotlist = ['ssrd_str',
          'clark',
          'josey2',
          'bignami']
# extract sst data
folder = 'C:/Users/nicol/source/repos/note_on_airsea/nns_annual/'# path to output files and data

sstname = 'cci_sst.csv' # SST observation file

sst_dat = pd.read_csv(os.path.join(folder,sstname),sep=',')                # xr.open_dataset(os.path.join(data_folder,sstname)) #_FA_ff0_fr0
sst_dat['time'] = pd.to_datetime(sst_dat['time'],format='%d/%m/%Y %H.%M')  # covert the string time records to datetime format

sst_dat = sst_dat.set_index(['time'])
sst_dat = xr.Dataset.from_dataframe(sst_dat) # convert to xarray dataset

fig, axes = plt.subplots(ncols=1, nrows=3)
plt.subplots_adjust(left=0.1,bottom=0.1,right=0.95,top=0.97,wspace=0.05, hspace=0.1)
simus_int = {}
for i, x in enumerate(methods):
    ds = xr.open_dataset(os.path.join(folder,'nns_'+ x +'.nc'), drop_variables=['z','zi','lon','lat'],engine='netcdf4') #_FA_ff0_fr0
    #ds.load()
    print(method_names[i])
    
    ds = ds.get(['temp'])
    ds['temp'] = ds['temp'].sel(z=109)
    ds['temp'] = ds['temp'].sel(lon=0)
    ds['temp'] = ds['temp'].sel(lat=0)
    simus_int[x] = ds['temp'].interp(time=sst_dat['time'],method='linear')
    if (x in plotlist):
        axes[0].plot(sst_dat['time'],simus_int[x],label=method_names[i], alpha=0.7)
        axes[1].plot(sst_dat['time'],(simus_int[x]-sst_dat['SST (degrees Celsius)']), alpha=0.7)
        axes[2].plot(sst_dat['time'],(simus_int[x]-sst_dat['SST (degrees Celsius)'])*100/sst_dat['SST (degrees Celsius)'], alpha=0.7)
    
tint = [dt.datetime.strptime('01/01/20','%d/%m/%y'),dt.datetime.strptime('01/01/24','%d/%m/%y')]
p1=axes[0].plot(sst_dat['time'],sst_dat['SST (degrees Celsius)'],label='data', alpha=0.7)
axes[0].fill_between(sst_dat['time'],sst_dat['standard error (degrees Celsius)']+sst_dat['SST (degrees Celsius)'],sst_dat['SST (degrees Celsius)']-sst_dat['standard error (degrees Celsius)'], color='grey', alpha=0.5)
axes[1].plot(tint,[0, 0])
axes[1].fill_between(sst_dat['time'],sst_dat['standard error (degrees Celsius)'],-sst_dat['standard error (degrees Celsius)'], color='grey', alpha=0.5)
axes[2].plot(tint,[0, 0])
axes[2].fill_between(sst_dat['time'],sst_dat['standard error (degrees Celsius)']*100/sst_dat['SST (degrees Celsius)'],-sst_dat['standard error (degrees Celsius)']*100/sst_dat['SST (degrees Celsius)'], color='grey',alpha=0.5)
axes[0].set_ylabel('SST (*C)',fontsize=12)#,fontweight='bold')
axes[1].set_ylabel('SST model - obs (*C)',fontsize=12)#,fontweight='bold')
axes[2].set_ylabel('Relative error (%)',fontsize=12)#,fontweight='bold')
axes[0].set_ylim([2.5,25])

axes[0].tick_params(labelbottom=False) 
axes[1].tick_params(labelbottom=False) 
#axes[0].set_yticks(fontsize=14)

axes[0].legend(ncol=6,frameon=False,loc='upper center')#,prop={'weight':'bold'})

# plot standard error, bias, r^2 comparing methods
stderr = {}
bias = {}
bias_percent = {}
r2s = {}
for i, x in enumerate(methods):
    stderr[method_names[i]] = np.mean(np.sqrt(np.square(sst_dat['SST (degrees Celsius)']-simus_int[x]))).item()
    bias[method_names[i]] = np.abs(np.mean(sst_dat['SST (degrees Celsius)']-simus_int[x])).item()
    bias_percent[method_names[i]] = np.mean((sst_dat['SST (degrees Celsius)']-simus_int[x])*100/sst_dat['SST (degrees Celsius)']).item()
    r2s[method_names[i]] = 1-np.sum(np.square(sst_dat['SST (degrees Celsius)']-simus_int[x])).item()/np.sum(np.square(simus_int[x]-np.mean(simus_int[x]).item())).item()

fig, axes = plt.subplots(ncols=1, nrows=3)
plt.subplots_adjust(left=0.15,bottom=0.2,right=0.95,top=0.98,wspace=0.05, hspace=0.075)
axes[0].bar(list(stderr),list(stderr.values()))
axes[0].set_ylabel('standard error \n (degrees Celsius)')
axes[1].bar(list(bias),list(bias.values()))
axes[1].set_ylabel('absolute bias \n (degrees Celsius)')
#axes[2].bar(list(bias_percent),list(bias_percent.values()))
#axes[2].set_ylabel('bias (%)')
axes[2].bar(list(r2s),list(r2s.values()))
axes[2].set_ylim([0.93,0.99])
axes[2].set_ylabel('R$^{2}$ value')
axes[0].tick_params(labelbottom=False)  
axes[1].tick_params(labelbottom=False)  
axes[2].tick_params(axis='x', labelrotation=90)
#axes[2].axis["bottom"].major_ticklabels.set_ha("right")

# #%%plot latent and sensible heat for the last year and for the two best methods - Clark and SSRD/STR

# methods = [#'berliand_berliand',
#            #'bignami',
#            'clark',
#            #'hastenrath_lamb',
#            #'josey1',
#            #'josey2',
#            #'ssr_str',
#            #'ssr_strd',
#            'ssrd_str'#,
#            #'ssrd_strd'
#            ]
# fig, axes = plt.subplots(ncols=2, nrows=2)
# qes = {}
# qhs = {}
# for i in methods:
#     ds = xr.open_dataset(os.path.join(folder,'nns_'+ i +'.nc'), drop_variables=['z','zi','lon','lat'],engine='netcdf4') #_FA_ff0_fr0
#     #ds.load()
#     print(i)

#     ds = ds.sel(time=slice("2023-01-01", "2024-01-01"))
#     ds = ds.get(['qe','qh'])
#     #ds['temp'] = ds['temp'].sel(z=109)
#     ds['qe'] = ds['qe'].sel(lon=0)
#     qes[i] = ds['qe'].sel(lat=0)
#     ds['qh'] = ds['qh'].sel(lon=0)
#     qhs[i] = ds['qh'].sel(lat=0)

#     axes[0,0].plot(ds['time'],qes[i])
#     axes[0,1].plot(ds['time'],qhs[i])
    
# axes[1,0].plot(ds['time'],qes['clark']-qes['ssrd_str'])
# axes[1,1].plot(ds['time'],qhs['clark']-qhs['ssrd_str'])
#     #axes[3].plot(ds['time'],qhs[i])
#     #only on first 
#     #axes[0,1].plot(sst_dat['time'],(simus_int[i]-sst_dat['SST (degrees Celsius)']))
    
# axes[0,0].legend(methods,ncol=2,frameon=False,loc='upper center',prop={'weight':'bold'})
# axes[0,1].legend(methods,ncol=2,frameon=False,loc='upper center',prop={'weight':'bold'})
# axes[0,0].set_ylabel('latent heat flux')
# axes[0,1].set_ylabel('sensible heat flux')
# axes[1,0].set_ylabel('latent heat flux clark - ssrd_str')
# axes[1,1].set_ylabel('sensible heat flux clark - ssrd_str')

# # compare other variables (ql net long wave radiation, internal swr, integrated swr, integrated heat, integrated total heat)
# # internal swr maybe at several depths? Or staggered depth profiles?

