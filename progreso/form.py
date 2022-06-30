from PyQt6.QtWidgets import QWidget, QFormLayout, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt
from widgets.lineEdits import (lineEdit, 
    lineEditCurrency,lineEditCurrencyWidget, dateWidget, lineEditPhone)
from widgets.widgets import textEdit, buttonWidget, labelWidget
from globalElements import constants, form_model


class main(form_model.main):
    def __init__(self, db):
        self.db = db

    def initiate_super(self):
        super().__init__(self.db)
        self.table = 'registros' #USE THIS TO SET SQL FROM HERE ----------------------------
        self.get_sql_update()
        self.title.setText('Detalles del Trámite')
        
    def configureForm(self):
        self.date_ = dateWidget(self.fontSize)
        self.title_ = lineEdit(self.fontSize)
        self.description_ = textEdit(self.fontSize)
        

        # for k,v in self.formItems.items():
        #     self.form_layout.addRow(labelWidget(k, self.fontSize), v)



        # self.form_layout.addRow(labelWidget('Id:', self.fontSize) ,self.id_)
        self.form_layout.addRow(self.file_)
        self.form_layout.addRow(labelWidget('Fecha:', self.fontSize) ,self.date_)
        self.form_layout.addRow(labelWidget('Título:', self.fontSize) ,self.title_)
        self.form_layout.addRow(labelWidget("Descripcion", 14, True, fontColor="Black", align="center"))
        self.form_layout.addRow(self.description_)
        # self.form_scroll_area.setWidget(self.form_widget)

        self.formItems = { 
            'id': self.id_, 
            'date_':self.date_,
            'title': self.title_, 
            'description_': self.description_,
            'file_': self.lineEditItems}


        
    


    
