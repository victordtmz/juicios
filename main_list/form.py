from PyQt6.QtWidgets import QWidget, QFormLayout, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt
from widgets.lineEdits import (lineEdit, 
    lineEditCurrency, dateWidget, lineEditPhone)
from widgets.widgets import textEdit, buttonWidget, labelWidget
from globalElements import constants, form_model


class main(form_model.main):
    def __init__(self):
        super().__init__()
        self.table = 'detalles' #USE THIS TO SET SQL FROM HERE ----------------------------
        
        
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
        self.formItems = {
            'id': self.id_, 
            'cliente': self.cliente, 
            'expediente':self.expediente, 
            'fecha_':self.fecha,
            'honorarios_': self.honorarios, 
            'telefono': self.telefono,
            'domicilio': self.domicilio,
            'domicilio1': self.domicilio1, 
            'ciudad':self.ciudad, 
            'estado':self.estado,
            'cp': self.cp, 
            'descripcion':self.description}

        # for k,v in self.formItems.items():
        #     self.form_layout.addRow(labelWidget(k, self.fontSize), v)



        # self.form_layout.addRow(labelWidget('Id:', self.fontSize) ,self.id_)
        self.form_layout.addRow(labelWidget('Cliente:', self.fontSize) ,self.cliente)
        self.form_layout.addRow(labelWidget('Expediente:', self.fontSize) ,self.expediente)
        self.form_layout.addRow(labelWidget('Fecha de inicio:', self.fontSize) ,self.fecha)
        self.form_layout.addRow(labelWidget('Honorarios:', self.fontSize) ,self.honorarios)
        self.form_layout.addRow(labelWidget('Telefono:', self.fontSize) ,self.telefono)
        self.form_layout.addRow(labelWidget('Domicilio:', self.fontSize) ,self.domicilio)
        self.form_layout.addRow(labelWidget('Domicilio:', self.fontSize) ,self.domicilio1)
        self.form_layout.addRow(labelWidget('Ciudad:', self.fontSize) ,self.ciudad)
        self.form_layout.addRow(labelWidget('Estado:', self.fontSize) ,self.estado)
        self.form_layout.addRow(labelWidget('Codigo postal:', self.fontSize) ,self.cp)
        self.form_layout.addRow(labelWidget("Descripcion", 14, True, fontColor="Black", align="center"))
        self.form_layout.addRow(self.description)


    
