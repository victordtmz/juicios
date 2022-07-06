from PyQt6.QtWidgets import QWidget, QFormLayout, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt
from widgets.lineEdits import (lineEdit, 
    lineEditCurrency,lineEditCurrencyWidget, dateWidget, lineEditPhone)
from widgets.widgets import textEdit, buttonWidget, labelWidget
from globalElements import constants
from globalElements.models import form


class main(form.main):
    def __init__(self):
        super().__init__()
    # def __init__(self):
        # super().__init__()
        # self.get_sql_update()
        # self.title.setText('Detalles del Trámite')
         
    def configureForm(self):
        
        self.cliente = lineEdit(self.fontSize)
        self.expediente = lineEdit(self.fontSize)
        self.fecha = dateWidget(self.fontSize)
        self.honorarios = lineEditCurrencyWidget(self.fontSize)
        self.telefono = lineEditPhone(self.fontSize)
        self.domicilio = lineEdit(self.fontSize)
        self.domicilio1 = lineEdit(self.fontSize)
        self.ciudad = lineEdit(self.fontSize)
        self.estado = lineEdit(self.fontSize)
        self.cp = lineEdit(self.fontSize)
        self.description = textEdit(self.fontSize)
        

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
        

        # self.form_scroll_area.setWidget(self.form_widget)

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

    

    def before_closing(self):
        self.save()
        self.db.connection.close() 

    def update_record(self, form_values:dict):
        """Update the record with the current form values
        """
        self.db.update_record_detalles(form_values)

    def insert_record(self,form_values:dict)->str:
        """Insert a new record with the current form values
        """
        self.db.insert_record_detalles(form_values)

    def create_table(self):
        """Call db function to update the correct record
        """
        self.db.create_table_detalles()

    def select_record(self):
        """Call db function to select the correct record
        """
        return self.db.select_detalles()