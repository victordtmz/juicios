from widgets.lineEdits import (lineEdit, dateWidget)
from widgets.widgets import textEdit, labelWidget
from globalElements.models import form

class main(form.main):
    def __init__(self, db):
        """extends form_model(extends QMainWindow)

        Args:
            db (sqlite db): db passed from main 
        """
        self.db = db
 
    def initiate_super(self):
        """callss super init function, placed here to be able to pass the db, required for init iu on form_model
        """
        super().__init__(self.db)
        self.table = 'registros' #USE THIS TO SET SQL FROM HERE ----------------------------
        self.get_sql_update()
        # self.title.setText('Detalles del Trámite')
        
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

    def get_sql_create_table(self) -> str:
        """Returns:
            str: CREATE TABLE sql
        """
        sql = f'''
        --sql
        CREATE TABLE IF NOT EXISTS {self.table} (
            id INTEGER PRIMARY KEY,
            date_ TEXT,
            title TEXT,
            description_ TEXT,
            file_ TEXT
            );
        '''
        return sql


        
    


    
