import os
from PyQt6.QtWidgets import QWidget, QFormLayout, QScrollArea, QSizePolicy, QMessageBox, QDialog, QSpacerItem, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from widgets.lineEdits import (lineEdit, 
    lineEditCurrency, dateWidget, lineEditPhone)
from widgets.widgets import textEdit, buttonWidget, labelWidget
from globalElements import constants
from widgets.comboBoxes import cbo
from widgets.radioButtons import activoRadioButtons

class main(QDialog):
    def __init__(self):
        super().__init__()
        self.fontSize = 14
        self.setMinimumWidth(600)
        # self.mode = 'new'
        self.iconEnlace = QIcon( f'{constants.DB_FILES}\icons\enlace_juicios.png')
        self.setWindowIcon(self.iconEnlace)
        self.configureForm()
        self.btn_cancel.pressed.connect(self.deleteLater)

    def configureForm(self):
        self.validate = labelWidget('', 13, fontColor='red')
        self.tipo = cbo(self.fontSize)
        self.expediente = lineEdit(self.fontSize)
        self.activo = activoRadioButtons()
        self.configure_buttons()

        
        # self.btnSave.setMinimumHeight(35)
        self.layout_ = QFormLayout()
        self.layout_.setVerticalSpacing(10)
        self.layout_.addRow(labelWidget('Tipo:', self.fontSize) ,self.tipo)
        self.layout_.addRow(labelWidget('Expediente:', self.fontSize) ,self.expediente)
        self.layout_.addRow(self.activo)
        self.layout_.addRow(self.validate)
        self.layout_.addRow(self.btn_widget)

        

        self.setLayout(self.layout_)

    def configure_buttons(self):
        self.btn_widget = QWidget()
        self.btn_widget_layout = QHBoxLayout()
        self.btn_widget.setLayout(self.btn_widget_layout)

        self.btn_save = buttonWidget('Guardar', 13, constants.iconSave, 'h1')
        self.btn_cancel = buttonWidget('Cacelar', 13, constants.iconCancel, 'h1')

        self.btn_widget_layout.addWidget(self.btn_cancel)
        self.btn_widget_layout.addWidget(self.btn_save)

    def get_info(self):
        tipo = self.tipo.getInfo()
        expediente = self.expediente.getInfo()
        activo = self.activo.getInfo()
        info = {'tipo':tipo, 'expediente':expediente, 'activo':activo}
        return info


    # def save_new(self):
        # tipo = self.tipo.getInfo()
        # expediente = self.expediente.getInfo()
        # if self.mode == 'new':
        #     database = f'{constants.ROOT_JUICIOS}\{tipo}\{expediente}'
        #     os.mkdir(database)
        #     return (tipo, expediente)
            # os.startfile(database)
