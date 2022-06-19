from PyQt6.QtWidgets import QWidget, QFormLayout
from PyQt6.QtCore import Qt
from globalElements.widgets.lineEdits import (lineEdit, 
    lineEditCurrency, dateWidget, lineEditPhone)
from globalElements.widgets.widgets import textEdit, buttonWidget, labelWidget
from globalElements import constants

class main(QWidget):
    def __init__(self):
        super().__init__()
        self.fontSize = 13
        self.configureForm()

    def configureForm(self):
        self.id_ = lineEdit(self.fontSize)
        self.id_.setReadOnly(True)
        self.cliente = lineEdit(self.fontSize)
        self.expediente = lineEdit(self.fontSize)
        self.fecha = dateWidget(self.fontSize)
        self.honorarios = lineEditCurrency(self.fontSize)
        self.telefono = lineEditPhone(self.fontSize)
        self.domicilio = lineEdit(self.fontSize)
        self.domicilio1 = lineEdit(self.fontSize)
        self.ciudad = lineEdit(self.fontSize)
        self.estado = lineEdit(self.fontSize)
        self.cp = lineEdit(self.fontSize)
        self.description = textEdit(self.fontSize)
        self.formItems = [self.id_, self.cliente, self.expediente, self.fecha, self.honorarios, 
            self.telefono, self.domicilio, self.domicilio1, self.ciudad, self.estado,
            self.cp, self.description]

        self.btnSave = buttonWidget('Guardar', 13, constants.iconSave)

        self.layout_ = QFormLayout()
        self.layout_.addRow(labelWidget('Id:', self.fontSize) ,self.id_)
        self.layout_.addRow(labelWidget('Cliente:', self.fontSize) ,self.cliente)
        self.layout_.addRow(labelWidget('Expediente:', self.fontSize) ,self.expediente)
        self.layout_.addRow(labelWidget('Fecha de inicio:', self.fontSize) ,self.fecha)
        self.layout_.addRow(labelWidget('Honorarios:', self.fontSize) ,self.honorarios)
        self.layout_.addRow(labelWidget('Telefono:', self.fontSize) ,self.telefono)
        self.layout_.addRow(labelWidget('Domicilio:', self.fontSize) ,self.domicilio)
        self.layout_.addRow(labelWidget('Domicilio:', self.fontSize) ,self.domicilio1)
        self.layout_.addRow(labelWidget('Ciudad:', self.fontSize) ,self.ciudad)
        self.layout_.addRow(labelWidget('Estado:', self.fontSize) ,self.estado)
        self.layout_.addRow(labelWidget('Codigo postal:', self.fontSize) ,self.cp)
        self.layout_.addRow(labelWidget("Descripcion", 14, True, fontColor="Black", align="center"))
        self.layout_.addRow(self.description)
        self.layout_.addRow(self.btnSave)

        # self.layoutBox = QWidget()
        # self.layoutBox.setMinimumWidth(460)
        self.setLayout(self.layout_)

        # self.layoutmain.addWidget(self.layoutBox)
        # self.layoutmain.setAlignment(self.layoutBox, Qt.AlignmentFlag.AlignHCenter) 
