# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 08:51:41 2020

@author: Carlos Jose Munoz
"""

from PyQt5.QtWidgets import QMainWindow,QMessageBox,QDialog,QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator

import numpy as np
import scipy.io as sio

class Ventanainicio(QDialog):
    def __init__(self):
        super(Ventanainicio, self).__init__();
        loadUi('ventana_inicio.ui',self)
        self.setup();

    def setup(self):
        self.botoningreso.accepted.connect(self.aceptar);
        self.botoningreso.rejected.connect(self.cancelar);
        self.Examinar.clicked.connect(self.browser);
        
    def asignarcontrolador(self, c):
        self.__mi_controlador = c
    
    def aceptar(self):
        if(self.matfile.isChecked()):
            tipefile=1
        elif (self.bcifile.isChecked()):
            tipefile=2
        else:
            tipefile=0
        
        self.__mi_controlador.recibirtipodearchivo(tipefile)
        
        if (tipefile==0):
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText('Message Error')
            msg.setWindowTitle('Message Box')
            msg.setInformativeText('Please, select a file type.')
            msg.show()
    
    def browser(self):
        archivo,_=QFileDialog.getOpenFileName(self, "Abrir senal","","Todos los archivos (*);;Archivos mat (*.mat)*;;Archivos OpenBCI (*.txt)*")
        self.__mi_controlador.recibirruta(archivo)
    
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
        self.Channel.setValidator(QIntValidator(1,8))
        self.tiempomenor.setValidator(QIntValidator(1,359000))
        self.tiempomayor.setValidator(QIntValidator(1,359000))
        self.new_signal.clicked.connect(self.cargarnueva);
        self.guardar_senales.clicked.connect(self.guardar);
        
        
    def asignarcontrolador(self, c):
        self.__mi_controlador = c
    
    def cargarnueva(self):
        if(self.matfile.isChecked()):
            tipefile=1
            archivo,_=QFileDialog.getOpenFileName(self, "Abrir senal","","Todos los archivos (*);;Archivos mat (*.mat)*")
            self.__mi_controlador.recibirruta(archivo)
            self.__mi_controlador.recibirtipodearchivo(tipefile)
            
        elif (self.bcifile.isChecked()):
            tipefile=2
            archivo,_=QFileDialog.getOpenFileName(self, "Abrir senal","","Todos los archivos (*);;Archivos OpenBCI (*.txt)*")
            self.__mi_controlador.recibirruta(archivo)
            self.__mi_controlador.recibirtipodearchivo(tipefile)
                     
        else:
            tipefile=0
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText('Message Error')
            msg.setWindowTitle('Message Box')
            msg.setInformativeText('Please, select a file type.')
            msg.show()
        
        
        
    def cargar(self):
        self.Channel.setText(str(0))
        mini, maxi=self.__mi_controlador.loadsignals(1)
        self.tiempomenor.setText(str(mini))
        self.tiempomayor.setText(str(maxi))
        
    def graficar(self):
        self.campo_graficacion.clear();
        channel=self.Channel.text()
        mini=self.tiempomenor.text()
        maxi=self.tiempomayor.text()
        senal=self.__mi_controlador.graph(int(channel),int(mini),int(maxi))
        if senal.ndim==1:
            self.campo_graficacion.plot(senal,pen=('r'))
        else:
            DC=500
            for canal in range (senal.shape[0]):                
                self.campo_graficacion.plot(senal[canal,int(mini):int(maxi)]+DC*canal,pen=('r'))       
        self.campo_graficacion.repaint()
        
        
    def filtrar(self):
        self.campo_graficacion.clear();
        if (self.one.isChecked() or self.mln.isChecked() or self.sln.isChecked()) and (self.universal.isChecked() or self.minimax.isChecked()) and (self.duro.isChecked() or self.suave.isChecked()) and (int(self.Channel.text())!=0):
            if (self.one.isChecked()):
                treshold=0
            elif (self.mln.isChecked()):
                treshold=1
            else:
                treshold=2
            
            if self.universal.isChecked():
                tw=0
            else:
                tw=1
            
            if self.duro.isChecked():
                tt=0
            else:
                tt=1
            
            senal,senalfiltrada=self.__mi_controlador.filtrar(int(self.Channel.text()),treshold,tw,tt)
            mini=int(self.tiempomenor.text())
            maxi=int(self.tiempomayor.text())
            self.campo_graficacion.plot(senal[mini:maxi]+20,pen=('r'))
            print(senalfiltrada)
            self.campo_graficacion.plot(senalfiltrada[mini : maxi],pen=('w'))
            
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText('Message Error')
            msg.setWindowTitle('Message Box')
            msg.setInformativeText('Please, select filter settings.')
            msg.show()
    
    def guardar (self):
        t=self.__mi_controlador.esposible()
        if t==1:
            archivo,_=QFileDialog.getSaveFileName(self, "Guardar archivo","","Todos los archivos (*);;Archivos mat (*.mat)*")
            channel=self.Channel.text()
            self.__mi_controlador.guardarfil(channel,archivo)
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText('Message Error')
            msg.setWindowTitle('Message Box')
            msg.setInformativeText('Please, filter a channel.')
            msg.show()