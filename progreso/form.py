from widgets.lineEdits import (lineEdit, dateWidget)
from widgets.widgets import textEdit, labelWidget
from globalElements.models import form 

class main(form.main):
    def __init__(self, db_folder):
        """extends form_model(extends QMainWindow)

        Args:
            db (sqlite db): db passed from main 
        """ 
        self._db_folder = db_folder
    def initiate_super(self):
        """callss super init function, placed here to be able to pass the db, required for init iu on form_model
        """
        super().__init__()
        self.db.set_db(self._db_folder)
        
    def configureForm(self):
        """Creates form widgets, places them on form layout.
         - creates a dictionary with formItems key == to the db row value, for easy data manipulation 
        """
        self.date_ = dateWidget(self.fontSize)
        self.title_ = lineEdit(self.fontSize)
        self.description_ = textEdit(self.fontSize)

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

    def before_closing(self):
        self.save()
        self.db.connection.close()

    def update_record(self, form_values:dict):
        """Update the record with the current form values
        """
        self.db.update_record_registros(form_values)

    def insert_record(self,form_values:dict)->str:
        """Insert a new record with the current form values
        """
        return self.db.insert_record_registros(form_values)

    def create_table(self):
        """Call db function to update the correct record
        """
        self.db.create_table_registros()

    # def select_record(self):
    #     """Call db function to select the correct record
    #     """
    #     return self.db.select_registros()


        
    


    
