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
import math

class ventanadentrada:
    def __init__(self):
        self.changepage=0
        self.channel=0 #0 para mostrar todos los canales
        self.tipeFile=0
        self.possiblesave=0
        
    def recibirruta (self, r):
        self.ruta=r
        
    def recibirtipodearchivo(self,tipefile):
        self.tipeFile=tipefile
        if (tipefile != 0):
            self.changepage=1
    
    def loadsignals(self, l):
        self.possiblesave=0
        print ('se cargo'+self.ruta)
        if (self.tipeFile==1):
            mat_contents = sio.loadmat(self.ruta)
            biosignal=mat_contents['data']
            sensores,puntos,ensayos=biosignal.shape
            self.biosignal=np.reshape(biosignal,(sensores,puntos*ensayos),order = 'F')
            mini=0
            maxi=359000
            
            
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
           mini=0
           maxi=8073
        return mini,maxi
    
    
    def graph(self,ch,m,mx):
        self.channel=ch
        if (self.channel==0):
            senal=self.biosignal
        if (self.channel!=0):
            senal= self.biosignal[self.channel-1,m:mx]
        return senal
    
    def transf_h (self, senal):
        wavelet =[-1/ np.sqrt(2), 1/np.sqrt(2)]
        scale=[1/np.sqrt(2), 1/np.sqrt(2)]
          
        #para calcular el numero de aproximaciones
        
        w=senal.shape[0]
        j= math.floor(np.log2((w/len(wavelet)))-1)
        j=j-6
        
        detalles=[]    
          
        for i in range (j):
                
            if (senal.shape[0]%2)!=0:        # Se añaden ceros para hacer la señal par
                senal=np.append(senal,0)
            
            aprox= np.convolve(senal, scale, 'full')
            aprox= aprox[1::2]      # a partir de la posicion 1 se toman cada dos valores
                                    # no se toma la posicion cero
            detail= np.convolve(senal, wavelet, 'full')
            detail= detail[1::2]
            
            detalles.append(detail)
          
            senal=aprox
    
        return (senal, detalles, j)

    def N (self, detalles, aprox):
        num=[]
        for i in range (len(detalles)):
            num.append(len(detalles[i]))
            suma=np.sum(num)
       
            num_samples= len(aprox)+ suma
        
        return(num_samples)
    
    def lam_uni (self,n):   
        lambda_uni= np.sqrt(2* np.log(n))
        return lambda_uni
    
    def lam_minimax (self,n):    
        lambda_mini= 0.3936 + (0.1829*(np.log(n))/(np.log(2)))
        return lambda_mini
    
    def umbral_duro(self,lambda_ , detail):
        for i in range (len(detail)):
            
            if np.absolute(detail[i])< lambda_:
                detail[i]= 0
          
        return detail
    
    def umbral_suave (self,lambda_, detail):
        for i in range (len(detail)):
            
            if detail[i]>= lambda_:
                detail[i]=np.sign (detail[i]*(np.absolute(detail[i])- lambda_))
                
            else: 
                detail[i]= 0
        return detail
    
    def reconstruir (self,aproximacion, details,j):    
        wavelet_inv = [1/np.sqrt(2) , -1/np.sqrt(2)];
        scale_inv = [1/np.sqrt(2) , 1/np.sqrt(2)];          
        
        for i in range(j-1):
        
            npoints_aprox = aproximacion.shape[0];
            Aprox_inv3 = np.zeros((2*npoints_aprox));
            Aprox_inv3[0::2] = aproximacion;
            Aprox_inv3[1::2] = 0;
            
            APROX3 = np.convolve(Aprox_inv3,scale_inv,'full');
            
            npoints_aprox = details[i].shape[0];
            Detail_inv3 = np.zeros((2*npoints_aprox));
            Detail_inv3[0::2] = details[i];
            Detail_inv3[1::2] = 0;
            
            DETAIL3 = np.convolve(Detail_inv3,wavelet_inv,'full');
            
            X3 = APROX3 + DETAIL3;
            print(i)
            #por la expansión de ceros se pueden aumentar las muestres       
            if X3.shape[0] > details[i+1].shape[0]:
                print("Quitando ceros");
                
                X3 = X3[0:details[i+1].shape[0]];
                
            aproximacion= X3
            
        npoints_aprox = aproximacion.shape[0];
        Aprox_inv3 = np.zeros((2*npoints_aprox));
        Aprox_inv3[0::2] = aproximacion;
        Aprox_inv3[1::2] = 0;
        
        APROX3 = np.convolve(Aprox_inv3,scale_inv,'full');
        
        npoints_aprox = details[j-1].shape[0];
        Detail_inv3 = np.zeros((2*npoints_aprox));
        Detail_inv3[0::2] = details[j-1];
        Detail_inv3[1::2] = 0;
        
        DETAIL3 = np.convolve(Detail_inv3,wavelet_inv,'full');
        
        X3 = APROX3 + DETAIL3;    
        return X3
#%%    
    def filtrar (self, ch, tr, tw, tt):
        self.possiblesave=1
        self.channel=ch
        signal=self.biosignal[ch,:]
        y=self.transf_h(signal)
        t=y[1]
        detalles_=t[::-1]#invierte el vector de detalles
        apromixacion=y[0]#ultima aproximacion
        j=y[2]
        
        n=self.N(detalles_,apromixacion)
        detalles_f=[]
#%%     duro   
        if (tr==0) and (tw==0) and (tt==0): #one, duro, universal
            for i in range(len(detalles_)):
                pr=self.lam_uni(n)
                detalles_f.append(self.umbral_duro(pr,detalles_[i]))
        
        if (tr==1) and (tw==0) and (tt==0): #mln, universal,duro
            for i in range(len(detalles_)):
                pr=self.lam_uni(n)
                sigma=(np.median(np.absolute(detalles_[i])))/0.6745
                pr=pr*sigma
                detalles_f.append(self.umbral_duro(pr,detalles_[i]))
        
        if (tr==2) and (tw==0) and (tt==0): #sln, universal, duro
            s=len(detalles_)-1
            sigma=(np.median(np.absolute(detalles_[s])))/0.6745
            for i in range(len(detalles_)):
                pr=self.lam_uni(n)
                detalles_f.append(self.umbral_duro(pr,detalles_[i]))
                
        if (tr==0) and (tw==1) and (tt==0): #one, minimax, duro
             for i in range(len(detalles_)):
                 pr=self.lam_minimax(n)
                 detalles_f.append(self.umbral_duro(pr,detalles_[i]))
                 
        if (tr==1) and (tw==1) and (tt==0):#mln, minimax, duro
            for i in range(len(detalles_)):
                pr=self.lam_minimax(n)
                sigma=(np.median(np.absolute(detalles_[i])))/0.6745
                pr=pr*sigma
                detalles_f.append(self.umbral_duro(pr,detalles_[i]))
                
        if (tr==2) and (tw==1) and (tt==0): #sln,minimax, duro
            s=len(detalles_)-1
            sigma=(np.median(np.absolute(detalles_[s])))/0.6745
            for i in range(len(detalles_)):
                pr=self.lam_minimax(n)
                detalles_f.append(self.umbral_duro(pr,detalles_[i]))
#%% suave                
        if (tr==0) and (tw==0) and (tt==1): #one, suave, universal
            for i in range(len(detalles_)):
                pr=self.lam_uni(n)
                detalles_f.append(self.umbral_suave(pr,detalles_[i]))
        
        if (tr==1) and (tw==0) and (tt==1): #mln, universal,suave
            for i in range(len(detalles_)):
                pr=self.lam_uni(n)
                sigma=(np.median(np.absolute(detalles_[i])))/0.6745
                pr=pr*sigma
                detalles_f.append(self.umbral_suave(pr,detalles_[i]))
        
        if (tr==2) and (tw==0) and (tt==1): #sln, universal, suave
            s=len(detalles_)-1
            sigma=(np.median(np.absolute(detalles_[s])))/0.6745
            for i in range(len(detalles_)):
                pr=self.lam_uni(n)
                detalles_f.append(self.umbral_suave(pr,detalles_[i]))
                
        if (tr==0) and (tw==1) and (tt==1): #one, minimax, suave
             for i in range(len(detalles_)):
                 pr=self.lam_minimax(n)
                 detalles_f.append(self.umbral_suave(pr,detalles_[i]))
                 
        if (tr==1) and (tw==1) and (tt==1):#mln, minimax, suave
            for i in range(len(detalles_)):
                pr=self.lam_minimax(n)
                sigma=(np.median(np.absolute(detalles_[i])))/0.6745
                pr=pr*sigma
                detalles_f.append(self.umbral_suave(pr,detalles_[i]))
                
        if (tr==2) and (tw==1) and (tt==1): #sln,minimax, suave
            s=len(detalles_)-1
            sigma=(np.median(np.absolute(detalles_[s])))/0.6745
            for i in range(len(detalles_)):
                pr=self.lam_minimax(n)
                detalles_f.append(self.umbral_suave(pr,detalles_[i]))
#%% final reconstruccion
        self.senalfiltrada=self.reconstruir(apromixacion,detalles_f,j)
        
        return self.biosignal[self.channel,:],self.senalfiltrada
    
    
    def guardarfil(self,ch,archivo):
        if self.possiblesave==1:
            sio.savemat(archivo,{'senalfiltrada': self.senalfiltrada,'canal':ch})
        
        
        
        
        
        
        
        
        
        
        
        
        
        