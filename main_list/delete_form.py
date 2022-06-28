import os
from tkinter.ttk import LabelFrame
from PyQt6.QtWidgets import QWidget, QFormLayout, QScrollArea, QSizePolicy, QMessageBox, QDialog, QSpacerItem, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from widgets.lineEdits import (lineEdit, 
    lineEditCurrency, dateWidget, lineEditPhone)
from widgets.widgets import textEdit, buttonWidget, labelWidget
from globalElements import constants
from widgets.comboBoxes import cbo

class main(QDialog):
    def __init__(self):
        super().__init__()
        self.fontSize = 16
        self.setMinimumWidth(500)
        # self.mode = 'new'
        self.iconEnlace = QIcon( f'{constants.DB_FILES}\icons\enlace_juicios.png')
        self.setWindowIcon(self.iconEnlace)
        self.setWindowTitle('Eliminar registro')
        self.configureForm()
        self.btn_cancel.pressed.connect(self.deleteLater)

    def configureForm(self):
        # self.warning = labelWidget('Para eliminar el registro seleccionado, proporcione la contraseña')
        self.pwd = lineEdit(self.fontSize)
        # self.resutMessage = labelWidget('')
        self.configure_buttons()

        
        # self.btnSave.setMinimumHeight(35)
        self.spacer = QSpacerItem(1,20)
        self.layout_ = QFormLayout()
        self.layout_.setVerticalSpacing(10)
        self.layout_.addRow(labelWidget('Para eliminar el registro seleccionado, proporcione la contraseña:', 13, False, 'Blue'))
        self.layout_.addRow(labelWidget('Contraseña:', self.fontSize) ,self.pwd)
        self.layout_.addItem(self.spacer)
        self.layout_.addRow(self.btn_widget)

        

        self.setLayout(self.layout_)

    def configure_buttons(self):
        self.btn_widget = QWidget()
        self.btn_widget_layout = QHBoxLayout()
        self.btn_widget.setLayout(self.btn_widget_layout)

        self.btn_delete = buttonWidget(' Eliminar', 13, constants.iconDelete, 'h1')
        self.btn_cancel = buttonWidget(' Cacelar', 13, constants.iconCancel, 'h1')

        self.btn_widget_layout.addWidget(self.btn_cancel)
        self.btn_widget_layout.addWidget(self.btn_delete)


