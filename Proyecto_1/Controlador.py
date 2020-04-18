# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 09:46:47 2020

@author: Carlos Jose Munoz
"""
# se importa el modelo y vista para que sesten comunicados por medio del controlador 
from Modelo import ventanadentrada
from Vista import Ventanainicio,dosventana

import sys

from PyQt5.QtWidgets import QApplication 

class Controlador(object): #objeto que va a recibir los comandos de la interfaz para enviarselos al modelo y desarrollar la accion necesaria 
    def __init__(self, vista,modelo,vista2): 
        self._mi_vista=vista #atributo para la apertura de la primera ventana 
        self._mi_modelo= modelo #apertura del modelo 
        self._mi2_ventana=vista2 #apertura de la segunda ventana 
        
    def recibirruta(self, r): #recibe la ruta del archivo  y se la pasa al modelo 
        self._mi_modelo.recibirruta(r)
    
    def recibirtipodearchivo(self, tipefile): #recibe el tipo de archivo para poder hacer el cambio de ventana
        self._mi_modelo.recibirtipodearchivo(tipefile)
        
        
    def loadsignals(self,l):#devuelve los valores iniciales de tiempo segun el tipo de señal 
        mini, maxi=self._mi_modelo.loadsignals(l)
        return mini, maxi
    
    def graph(self,ch,m,mx): #retorna la señal (todos o un solo canal) y los valores de tiempo que se vana graficar 
        senal= self._mi_modelo.graph(ch,m,mx)
        return senal
    
    def filtrar(self,ch,tr,tw,tt): #retorna la señal (canal) original y la señal filtrada que devuelve el modelo dependiendo del tipo del filtro 
        senal, senalfiltrada= self._mi_modelo.filtrar(ch,tr,tw,tt)
        return senal, senalfiltrada
    
    def guardarfil(self,ch,archivo): #recibe la ruta, nombre de archivo y canal para guardar la señal filtrada  
        self._mi_modelo.guardarfil(ch,archivo)
    
    def esposible(self): #habilita el botón de guardar señal filtrada 
        return self._mi_modelo.possiblesave
        
if __name__ == '__main__': #inicio del programa, es el programa principal que se corre 
    app=QApplication(sys.argv)
    mi_vista=Ventanainicio(); #objeto asociado a la ventana inicial 
    mi_modelo=ventanadentrada();# objeto asociado al modelo 
    mi_2vista=dosventana(); #objeto asociado a la ventana de visualizacion 
    mi_controlador= Controlador(mi_vista,mi_modelo,mi_2vista)# objeto que enlaza las ventanas con los modelos 
    
    #asignarle el controlador a la vista
    mi_vista.asignarcontrolador(mi_controlador) #se usa para realizar el enlace entre la vista y el controlador 
    
    mi_vista.show()  #genera la ventana inicial 
    
        
    app.exec_();
    if (mi_modelo.changepage==1): #si es posible pasar a la segunda ventana se genera la ventana secundaria 
        
        mi_2vista.asignarcontrolador(mi_controlador)
        
        mi_2vista.show();
        sys.exit(app.exec_());
    
 print ('hola mundo')


    
