# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 15:16:46 2020

@author: Carlos Jose Munoz
"""

import scipy.io as sio
import matplotlib.pyplot as plt 
import numpy as np
import scipy.signal as signal
from math import sqrt as r2

def rms(x):
    N=len(x)
    suma=0
    vrms=0
    for i in x:
        suma=(i*i)+suma
       
    vrms=r2(suma/N)
    return vrms

mat_contents= sio.loadmat('signals.mat')
print("Los campos cargados son: "+ str(mat_contents.keys()))

ECG= np.squeeze(mat_contents['ECG_asRecording'])
ECGfilter= np.squeeze(mat_contents['ECG_filtered'])

EMG1=np.squeeze(mat_contents['EMG_asRecording1']);
EMG1filtered=np.squeeze(mat_contents['EMG_filtered1']);

EMG1=np.squeeze(mat_contents['EMG_asRecording2']);
EMG1filtered=np.squeeze(mat_contents['EMG_filtered2']);


#se obtiene el valor de la freuencia, y el vectorde tiempo
frecuencia=np.squeeze(mat_contents['Fs'])
print('tipo de variable frecuencia: '+ str(type(frecuencia)))
print (frecuencia)

t=np.arange(0, (len(ECG)/frecuencia), 1/frecuencia)


#Se obtiene los graficos de la señal filtrada y sin filtrar 
plt.plot(t,ECG, label='ECG sin filtrar')
plt.plot(t,ECGfilter, label='ECG filtrada')
plt.title('ECG')
plt.xlabel('tiempo(s)')
plt.ylabel('Amplitud(v)')
plt.legend()
plt.savefig('ECG_filterandnot')
plt.show()

##Se puede observar en los gráficos que el filtro es un pasa altas, el cual le quital el nivel dc a la señal

#se hace la gráfica de un ciclo cardíaco para la señal sin filtrar 
plt.plot(t[0:819],ECG[0:819], label='ECG sin filtrar')
plt.title('ciclo cardiaco ECG sin filtrar')
plt.xlabel('tiempo(s)')
plt.ylabel('Amplitud(v)')
plt.legend()
plt.show()

#Se encuentra el valor RMS, la media y la varianza de la ECG sin filtrada
varianza=np.var(ECG[0:819])
deviacion=np.std(ECG[0:819])
Vrms=rms(ECG[0:819])


#se hace la gráfica de un ciclo cardíaco para la señal filtrada
plt.plot(t[0:819],ECGfilter[0:819], label='ECG filtrada')
plt.title('ciclo cardiaco ECG filtrada')
plt.xlabel('tiempo(s)')
plt.ylabel('Amplitud(v)')
plt.legend()
plt.show()

#Se encuentra el valor RMS, la media y la varianza de la ECG filtrada
varianza1=np.var(ECGfilter[0:819])
deviacion1=np.std(ECGfilter[0:819])
Vrms1=rms(ECGfilter[0:819])

print (str(varianza) + " vs " + str(varianza1))
print (str(deviacion) + " vs " + str(deviacion1))
print (str(Vrms) + " vs " + str(Vrms1))