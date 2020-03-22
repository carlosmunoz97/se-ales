# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 08:51:41 2020

@author: Carlos Jose Munoz
"""

from PyQt5.QtWidgets import QMainWindow,QMessageBox,QDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator

class Ventanainicio(QDialog):
    def __init__(self):
        super(Ventanainicio, self).__init__();
        loadUi('ventana_inicio.ui',self)
        self.setup();

    def setup(self):
        self.botoningreso.accepted.connect(self.aceptar);
        self.botoningreso.rejected.connect(self.cancelar);
        
    def asignarcontrolador(self, c):
        self.__mi_controlador = c
    
    def aceptar(self):        
        #recibir los datos de la interfaz
        ruta= self.ruta.text()
        if(self.matfile.isChecked()):
            tipefile=1
        elif (self.bcifile.isChecked()):
            tipefile=2
        else:
            tipefile=0
           
        self.__mi_controlador.recibirruta(ruta, tipefile)
        if (tipefile==0):
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText('Message Error')
            msg.setWindowTitle('Message Box')
            msg.setInformativeText('Please, select a file type.')
            msg.show()
        
    def cancelar(self):
        pass;

class dosventana (QMainWindow):
    def __init__(self):
        super(dosventana,self).__init__();
        loadUi('interfaz.ui',self)
        self.setup();
    def setup(self):
        self.Carga.clicked.connect(self.cargar);
        self.Graficar.clicked.connect(self.graficar);
        self.Filtrar.clicked.connect(self.filtrar)
        
        self.Channel.setValidator(QIntValidator(1,9))
        
    def asignarcontrolador(self, c):
        self.__mi_controlador = c
        
    def cargar(self):
        self.__mi_controlador.loadsignals(1)
        
    def graficar(self):
        #channel=self.Channel.text()
        #self.__mi_controlador.graph(1,channel)
        pass;
        
    def filtrar(self):
        print ('filtrar')
        pass;
        