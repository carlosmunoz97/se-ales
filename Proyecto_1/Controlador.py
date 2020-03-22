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
        
    def recibirruta(self, r,tf):
        self._mi_modelo.recibirruta(r,tf)
    
    def loadsignals(self,l):
        self._mi_modelo.loadsignals(l)
    
    #def graph(self,l,ch):
     #   self._mi_modelo.channel=ch
     #  self.graph(l)
        
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
    
    

    