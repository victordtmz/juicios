from PyQt6.QtWidgets import QWidget, QFormLayout, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt
from widgets.lineEdits import (lineEdit, 
    lineEditCurrency, dateWidget, lineEditPhone)
from widgets.widgets import textEdit, buttonWidget, labelWidget
from globalElements import constants

class main(QScrollArea):
    def __init__(self):
        super().__init__()
        self.fontSize = 13
        self.setWidgetResizable(True)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.configureForm()

    def configureForm(self):
        self.formValues = []
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
        self.formItems = (self.id_, self.cliente, self.expediente, self.fecha, self.honorarios, 
            self.telefono, self.domicilio, self.domicilio1, self.ciudad, self.estado,
            self.cp, self.description)

        

        self.btnSave = buttonWidget('Guardar', 13, constants.iconSave, 'h2')
        # self.btnSave.setMinimumHeight(35)

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


        self.layoutBox = QWidget()
        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layoutBox.setMaximumWidth(600)
        self.layoutBox.setLayout(self.layout_)
        self.setWidget(self.layoutBox)


        # for widget in self.layout_.rowCount():
        #     print(widget)

        # self.layoutmain.addWidget(self.layoutBox)
        # self.layoutmain.setAlignment(self.layoutBox, Qt.AlignmentFlag.AlignHCenter) 
    def clear(self):
        for i in self.formItems:
            i.reSet()

    def populate(self, content):
        index = 0
        for i in self.formItems:
            i.populate(content[index])
            index += 1

    # def form_values_populate(self):
    #     for i in self.formItems:
    #         self.formValues.append(i.getDbInfo())

    def get_info(self):
        return list(map(lambda x: x.getDbInfo(), self.formItems))