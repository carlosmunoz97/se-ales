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

class Ventanainicio(QDialog): #venatana de inicio para escoger el tipo y la ruta del archivo 
    def __init__(self): #abre la ventana inicial 
        super(Ventanainicio, self).__init__();
        loadUi('ventana_inicio.ui',self)
        self.setup();

    def setup(self): #define los procesos que se realizaran si se presiona uno u otro boton 
        self.botoningreso.accepted.connect(self.aceptar);
        self.botoningreso.rejected.connect(self.cancelar);
        self.Examinar.clicked.connect(self.browser);
        
    def asignarcontrolador(self, c):# se crea el enlace entre esta ventana y el controlador 
        self.__mi_controlador = c
    
    def aceptar(self): #se valida que se haya escogido un tipo de archivo, si no se ha escogido ruta, no va a graficar nada en la ventana de visualizacion
        if(self.matfile.isChecked()):
            tipefile=1
        elif (self.bcifile.isChecked()):
            tipefile=2
        else:
            tipefile=0
        
        self.__mi_controlador.recibirtipodearchivo(tipefile)
        
        if (tipefile==0): #genera un mensaje si no se ha seleccionado un tipo de archivo, y cierra el programa  
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText('Message Error')
            msg.setWindowTitle('Message Box')
            msg.setInformativeText('Please, select a file type.')
            msg.show()
    
    def browser(self): #boton para definir la ruta donde se encuentra el archivo 
        archivo,_=QFileDialog.getOpenFileName(self, "Abrir senal","","Todos los archivos (*);;Archivos mat (*.mat)*;;Archivos OpenBCI (*.txt)*")
        self.__mi_controlador.recibirruta(archivo)
    
    def cancelar(self): #cierra la ventana 
        pass;

class dosventana (QMainWindow): #ventana de visualizacion 
    def __init__(self):#carga la ventana 
        super(dosventana,self).__init__();
        loadUi('interfaz.ui',self)
        self.setup();
    def setup(self): #genera las acciones de los botones y widgets en la interfaz
        self.Carga.clicked.connect(self.cargar);
        self.Graficar.clicked.connect(self.graficar);
        self.Filtrar.clicked.connect(self.filtrar)        
        self.Channel.setValidator(QIntValidator(1,8))
        self.tiempomenor.setValidator(QIntValidator(1,359000))
        self.tiempomayor.setValidator(QIntValidator(1,359000))
        self.new_signal.clicked.connect(self.cargarnueva);
        self.guardar_senales.clicked.connect(self.guardar);
        
        
    def asignarcontrolador(self, c): #se crea un enlace ocn el controlador 
        self.__mi_controlador = c
    
    def cargarnueva(self): #carga una nueva señal, solo si ya se ha escogido el tipo de archivo 
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
                     
        else: #genera mensaje si no se ha escogido un tipo de archivo 
            tipefile=0
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText('Message Error')
            msg.setWindowTitle('Message Box')
            msg.setInformativeText('Please, select a file type.')
            msg.show()
        
        
        
    def cargar(self): #permite cargar el archivo  definiendo los valores iniciales  de tiempo y  valor 0 en el campo e canales 
        self.Channel.setText(str(0))
        mini, maxi=self.__mi_controlador.loadsignals(1)
        self.tiempomenor.setText(str(mini))
        self.tiempomayor.setText(str(maxi))
        
    def graficar(self): #genera la grafica  teniendo en cuenta que canal graficar y el tiempo que define el usuario
        self.campo_graficacion.clear();
        channel=self.Channel.text()
        mini=self.tiempomenor.text()
        maxi=self.tiempomayor.text()
        senal=self.__mi_controlador.graph(int(channel),int(mini),int(maxi))
        if senal.ndim==1: # si solo se grafica un canal 
            self.campo_graficacion.plot(senal,pen=('r'))
        else: #si se grafican todos los canales 
            DC=500
            for canal in range (senal.shape[0]):                
                self.campo_graficacion.plot(senal[canal,int(mini):int(maxi)]+DC*canal,pen=('r'))       
        self.campo_graficacion.repaint()
        
        
    def filtrar(self): #genera el filtrado, si y solo si se ha escogido un canal y se ha realizado la configuracion del filtro 
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
    
    def guardar (self): #se permite guardar una señal filtrada si y solo si ya ha sido realizado el filtro 
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