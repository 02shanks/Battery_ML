import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
from scipy.signal import argrelextrema

f1=pd.read_csv(r'C:\Users\Admin\sagas\oorjaenergy\Severson-et-al\UL-PUR_R20-OV1_18650_NCA_23C_2.5-96.5_0.5-0.5C_a_timeseries.csv')
l=[]
k=[]
for i in range(1,len(f1['Current (A)'])-1):
    v_prev=f1['Current (A)'][i-1]
    v=f1['Current (A)'][i]
    next_v=f1['Current (A)'][i+1]
    dv1=v-v_prev
    dv2=next_v-v
    if abs(dv1+dv2)<0.2 and abs(dv1)>0.1 and abs(dv2)>0.1 :  
        k.append((v_prev,v,next_v))
        l.append(i)
mins=argrelextrema(f1['Current (A)'].values,np.less_equal,order=3)[0]
maxs=argrelextrema(f1['Current (A)'].values,np.greater_equal,order=3)[0]
m=[p for p in mins if f1['Current (A)'][p]<-1.7]
x=[p for p in maxs if f1['Current (A)'][p]>1.7]
l=l+m+x
print(f'Number of values in l : {len(l)}')
print(f'Number of values in k : {len(k)+len(m)+len(x)}')
bdata_fin= f1.drop(l)
for i in range(0,len(bdata_fin),1000):
    plt.plot(bdata_fin['Current (A)'][i:i+1000])
    plt.show()
bdata_fin.to_csv(r'C:\Users\Admin\sagas\oorjaenergy\Severson-et-al\Cleaned files\cleaned_UL-PUR_R20-OV1_18650_NCA_23C_2.5-96.5_0.5-0.5C_a_timeseries.csv',index=False)