# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 20:00:44 2020

@author: Usuario
"""

import numpy as np
import matplotlib.pyplot as plt
from csv import reader as reader_csv
import scipy.signal as signal
import scipy.io as sio

class ventanadentrada:
    def __init__(self):
        self.changepage=0
        self.channel=0 #0 para mostrar todos los canales
        self.tipeFile=0
        
    def recibirruta (self, r, tf):
        self.ruta=r
        self.tipeFile=tf
        if (tf!=0):
            self.changepage=1
    
    def loadsignals(self, l):
        if (self.tipeFile==1):
            mat_contents = sio.loadmat(self.ruta)
            self.biosignal=mat_contents['data']
        if (self.tipeFile==2):
           data=open(self.ruta,'r');
           lines = reader_csv(data);
           
           row_number=0
           header='';
           channels=11;
           header_size = 6;
           
           data =[]
           for row in lines:
               if row_number < header_size:
                   header=header+row[0]+'\n';
                   row_number = row_number +1 ;
               else:
                   temp=[]
                   counter=0;
                   for colum in row:
                       if counter==0:
                           counter=counter+1;
                           continue;
                       elif counter== channels+1:
                           break;
                       else:
                           temp.append(float(colum));
                       counter=counter+1;
                   data.append(temp)
           biosignal=np.asarray(data,order= 'C')
           self.biosignal=np.transpose(biosignal)
           print("la señal ha sido cargada")
           
 #   def graph(self,l):
                                  
            
