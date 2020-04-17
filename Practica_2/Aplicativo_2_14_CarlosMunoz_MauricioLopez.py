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
from tabulate import tabulate

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

##Datos de EMG de Triceps
EMG1=np.squeeze(mat_contents['EMG_asRecording1']);
EMG1filtered=np.squeeze(mat_contents['EMG_filtered1']);

##Datos de EMG de Biceps
EMG2=np.squeeze(mat_contents['EMG_asRecording2']);
EMG2filtered=np.squeeze(mat_contents['EMG_filtered2']);


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
plt.plot(t[0:2000],ECG[0:2000], label='ECG sin filtrar')
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
plt.plot(t[0:2000],ECGfilter[0:2000], label='ECG filtrada')
plt.title('ciclo cardiaco ECG filtrada')
plt.xlabel('tiempo(s)')
plt.ylabel('Amplitud(v)')
plt.legend()
plt.show()

#Se encuentra el valor RMS, la media y la varianza de la ECG filtrada
varianza1=np.var(ECGfilter[0:819])
deviacion1=np.std(ECGfilter[0:819])
Vrms1=rms(ECGfilter[0:819])

print ('la varianza de ECG sin filtrar es: ' + str(varianza)+' y la de ECG filtrada es: ' + str(varianza1))
print('la desviacón de ECG sin filtrar es: '+ str(deviacion)+' y la de ECG filtrada es: '+ str(deviacion1))
print('El valor RMS de ECG sin filtrar es: '+str(Vrms)+'y el de ECG filtrada es: '+str(Vrms1))

#Extracción de los 15 ciclos y comparacion
vector_estadisticas=[]
vector_ciclos=[]
for i in range (0,15):
    vector_ciclos.append(ECGfilter[819*i:819*(i+1)])
    vector_estadisticas.append([i+1,np.var(ECGfilter[819*i:819*(i+1)]),np.std(ECGfilter[819*i:819*(i+1)])])
    plt.plot(t[819*i:819*(i+1)],ECGfilter[819*i:819*(i+1)], label='ECG filtrada')
    plt.title('ciclo cardiaco ECG filtrada')
    plt.xlabel('tiempo(s)')
    plt.ylabel('Amplitud(v)')
    plt.legend()
    plt.show()
    
print(tabulate(vector_estadisticas, headers=['ciclo','varianza','desviación estandar']))
#-----------------------------------------------------------------------------------------------#
#se realiza el analisis para las señales de biceps y triceps
#se creo el vector tiempo para las señales EMG1 y EMG2 
print("El tiempo de duracion de las señales es: "+ str(1/frecuencia*(len(EMG1))))
tp=np.arange(0, (len(EMG1)/frecuencia), 1/frecuencia)##se crea un vector de tiempo.
## Grafica de la señal Triceps(EMG1) sin filtrar y filtrada
plt.figure()
plt.plot(tp,EMG1, label='EMG Triceps sin filtrar')
plt.plot(tp,EMG1filtered, label='EMG Triceps filtrada')
plt.title('EMG Triceps')
plt.xlabel('tiempo(s)')
plt.ylabel('Amplitud(v)')
plt.legend()
plt.show()

## Grafica de la señal Biceps(EMG2) sin filtrar y filtrada
plt.figure()
plt.plot(tp,EMG2, label='EMG Biceps sin filtrar')
plt.plot(tp,EMG2filtered, label='EMG Biceps filtrada')
plt.title('EMG Biceps')
plt.xlabel('tiempo(s)')
plt.ylabel('Amplitud(v)')
plt.legend()
plt.show()

#Se toma un tramo de contraccion para las señales filtradas y se calcula el promedio, valor RMS,varianza y desviacion estandar.
plt.figure()
plt.plot(tp[2500:5100],EMG1filtered[2500:5100], label='EMG Triceps filtrada')
plt.title("Tramo de contraccion EMG Triceps ")
plt.xlabel('tiempo(s)')
plt.ylabel('Amplitud(v)')
plt.legend()
plt.show()
print("El promedio es "+str(np.mean(EMG1filtered[2500:5100])))
print("El Valor RMS es "+str(rms(EMG1filtered[2500:5100])))
print("La varianza es "+str(np.var(EMG1filtered[2500:5100])))
print("La desviacion estandar es "+str(np.std(EMG1filtered[2500:5100])))
print("............................................................")

plt.figure()
plt.plot(tp[2500:5100],EMG2filtered[2500:5100], label='EMG Biceps filtrada')
plt.title("Tramo de contraccion EMG Biceps ")
plt.xlabel('tiempo(s)')
plt.ylabel('Amplitud(v)')
plt.legend()
plt.show()
print("El promedio es "+str(np.mean(EMG2filtered[2500:5100])))
print("El Valor RMS es "+str(rms(EMG2filtered[2500:5100])))
print("La varianza es "+str(np.var(EMG2filtered[2500:5100])))
print("La desviacion estandar es "+str(np.std(EMG2filtered[2500:5100])))


##para el biceps filtrado 
vectorBiceps_estadisticas=[]
vectorBiceps_ciclos=[]
for i in range (0,12):
    vectorBiceps_ciclos.append(EMG2filtered[2500*i:2500*(i+1)])
    vectorBiceps_estadisticas.append([i+1,np.var(EMG2filtered[2500*i:2500*(i+1)]),np.mean(EMG2filtered[2500*i:2500*(i+1)])])
    plt.plot(t[2500*i:2500*(i+1)],EMG2filtered[2500*i:2500*(i+1)], label='EMG biceps filtrada')
    plt.title('ciclo EMG biceps filtrada')
    plt.xlabel('tiempo(s)')
    plt.ylabel('Amplitud(v)')
    plt.legend()
    plt.show()
    
print(tabulate(vectorBiceps_estadisticas, headers=['ciclo bi','varianza','valor promedio']))

##Para el triceps filtrado
vectorTri_estadisticas=[]
vectorTri_ciclos=[]
for i in range(0,12):
    vectorTri_ciclos.append(EMG1filtered[2500*i:2500*(i+1)])
    vectorTri_estadisticas.append([i+1,np.var(EMG1filtered[2500*i:2500*(i+1)]),np.mean(EMG1filtered[2500*i:2500*(i+1)])])
    plt.plot(t[2500*i:2500*(i+1)],EMG1filtered[2500*i:2500*(i+1)], label='EMG triceps filtrada')
    plt.title('ciclo EMG triceps filtrada')
    plt.xlabel('tiempo(s)')
    plt.ylabel('Amplitud(v)')
    plt.legend()
    plt.show()
    
print(tabulate(vectorTri_estadisticas, headers=['ciclo tri','varianza','valor promedio']))
