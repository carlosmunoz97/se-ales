# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 09:46:47 2020

@author: Carlos Jose Munoz
"""

from Modelo import ventanadentrada
from Vista import Ventanainicio,dosventana

import sys

from PyQt5.QtWidgets import QApplication 

class Controlador(object):
    def __init__(self, vista,modelo,vista2):
        self._mi_vista=vista
        self._mi_modelo= modelo
        self._mi2_ventana=vista2
        
    def recibirruta(self, r):
        self._mi_modelo.recibirruta(r)
    
    def recibirtipodearchivo(self, tipefile):
        self._mi_modelo.recibirtipodearchivo(tipefile)
        
        
    def loadsignals(self,l):
        mini, maxi=self._mi_modelo.loadsignals(l)
        return mini, maxi
    
    def graph(self,ch,m,mx):
        senal= self._mi_modelo.graph(ch,m,mx)
        return senal
    
    def filtrar(self,ch,tr,tw,tt):
        senal, senalfiltrada= self._mi_modelo.filtrar(ch,tr,tw,tt)
        return senal, senalfiltrada
    
    def guardarfil(self,ch,archivo):
        self._mi_modelo.guardarfil(ch,archivo)
    
    def esposible(self):
        return self._mi_modelo.possiblesave
        
if __name__ == '__main__':
    app=QApplication(sys.argv)
    mi_vista=Ventanainicio();
    mi_modelo=ventanadentrada();
    mi_2vista=dosventana();
    mi_controlador= Controlador(mi_vista,mi_modelo,mi_2vista)
    
    #asignarle el controlador a la vista
    mi_vista.asignarcontrolador(mi_controlador)
    
    mi_vista.show()  
    
        
    app.exec_();
    if (mi_modelo.changepage==1):
        
        mi_2vista.asignarcontrolador(mi_controlador)
        
        mi_2vista.show();
        sys.exit(app.exec_());
    
    

    