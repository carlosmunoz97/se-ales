# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 08:51:41 2020

@author: Carlos Jose Munoz
"""

from PyQt5.QtWidgets import QMainWindow,QMessageBox,QDialog
from PyQt5.uic import loadUi

class Ventanainicio(QDialog):
    def __init__(self):
        super(Ventanainicio, self).__init__();
        loadUi('interfaz.ui',self)
        self.setup();
