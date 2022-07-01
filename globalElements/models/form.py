from abc import abstractmethod
from PyQt6.QtWidgets import QMainWindow,QStatusBar, QWidget, QFormLayout, QScrollArea, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from widgets.lineEdits import (lineEdit)
from widgets.widgets import buttonWidget
from globalElements import constants

class main(QMainWindow):
    """extends QMainWinidow
        - Model to be used for all forms - contains necessary methods and components to interact with main list, get elements directly from db and save directly to db. 

        Args:
            db (sqlite or mySql): Databased to be used in connection with form.
        """
    def __init__(self, db):
        
        super().__init__()
        self.table = ''
        self.db = db
        self.fontSize = 13
        self.dirty = False
        self.init_model_ui()
        self.get_sql_new()
        
    
    def init_model_ui(self):
        """call methods and create elements in ordered to be used when instatiating object. 
        """
        self.id_ = lineEdit(self.fontSize)
        self.id_.setReadOnly(True)
        self.status_bar = QStatusBar()
        self.status_bar.setContentsMargins(0,0,0,0)
        self.setStatusBar(self.status_bar)
        self.configure_layout()
        self.configureForm()
        self.set_main_connections()


    def configure_layout(self):
        """Configures all elements and places them on the main layout. 
        """
        # self.title = labelWidget('Formulario', 18, True, 'white', 'center', '#002142', '5px')
        #form items layout
        self.form_widget = QWidget()
        self.form_widget.setMaximumWidth(600)
        self.form_widget.setMinimumWidth(550)
        self.form_layout = QFormLayout()
        
        
        self.form_widget.setLayout(self.form_layout)
        self.form_scroll_area = QScrollArea()
        self.form_scroll_area.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # self.form_scroll_area.setpo
        self.form_scroll_area.setStyleSheet(('''QScrollArea {border-style: none;};'''))
        self.form_scroll_area.setWidgetResizable(True)
        # self.form_scroll_area.setmin
        # self.layout_.setAlignment(self.form_scroll_area, Qt.AlignmentFlag.AlignHCenter)

        self.form_scroll_area.setWidget(self.form_widget)
        

        #save and cancel buttons
        self.btn_widget = QWidget()
        self.btn_layout = QHBoxLayout()
        self.btn_widget.setLayout(self.btn_layout)
        self.btn_save = buttonWidget('Guardar', 13, constants.iconSave, 'h2_form')
        self.btn_cancel = buttonWidget('Cancelar', 13, constants.iconCancel, 'h2_form',)
        self.btn_layout.addWidget(self.btn_cancel)
        self.btn_layout.addWidget(self.btn_save)
        self.btn_widget.setMaximumWidth(550)

        #main layout
        self.widget_ = QWidget()
        # self.setWidget(self.widget_)
        self.setCentralWidget(self.widget_)
        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0,0,0,0)
        self.widget_.setLayout(self.layout_)
        # self.layout_.addWidget(self.title)
        self.layout_.addWidget(self.form_scroll_area)
        self.layout_.addWidget(self.btn_widget)
        self.layout_.setAlignment(self.btn_widget ,Qt.AlignmentFlag.AlignHCenter)

    @abstractmethod
    def configureForm(self):
        """abstract method: set all form widgets, place them on form layout and create the self.formItems dict with such widgets. 
        """
        self.formItems = {}

        
    def clear(self):
        """iterate through all widgets in self.formItes values and sets to default or ''
        """
        for i in self.formItems.values():
            i.reSet()

    def populate(self, record:dict = {}): 
        """Populates the form, a dict with values may be passed, else, it will collect the information from the Database

        Args:
            record (dict, optional): key => db column id. value => value to be inserted in corresponding widget. 
        """
        if not record:
            sql = f''' --sql
            SELECT * FROM {self.table};''' 
            try: record = self.db.select_dict(sql)
            except: return
            
            if record:
                record = record[0]
        try: 
            for k, v in self.formItems.items():
                try: v.populate(record[k])
                except: v.clear()
        except: 
            self.clear()

    def set_main_connections(self):
        """sets all widget connections, including:(event:save, signal:self.destroyed)
        """
        self.destroyed.connect(self.save)
        for i in self.formItems.values():
            i.editingFinished.connect(self.set_form_dirty)
    
    def set_form_dirty(self):
        """sets self.dirty to True.
        signal: editingFinished - all of self.formItems widgets 
        """
        self.dirty = True
    
    @abstractmethod
    def get_sql_create_table(self) -> str:
        """abstract method - contains sql 
        Returns:
            str: sql to create table on db that is used in this form.

        """
        sql = ''
        return sql

    def get_sql_update(self):
        """uses self.formItems dict to create the sql with column names (keys) and values (widget value) for UPDATE

        Returns:
            str: sql to UPDATE current record with the form values.
        """
        values = ''
        items = self.formItems.copy()
        del items['id']
        for k,v in items.items():
            value = v.getDbInfo()
            values += f"{k} = '{value}',"
        values = values[:-1]
        
        sql = f'''
            --sql
            UPDATE {self.table} SET {values} WHERE id = ?;
            '''

        return sql

    def get_sql_new(self) -> str:
        """uses self.formItems dict to create the sql with column names (keys) and values (widget value)

        Returns:
            str: sql to insert a new record with the form values.
        """
        values = ''
        columns = ''
        #create a copy of formItems dict
        items = self.formItems.copy()
        #remove id form copy
        del items['id']
        #from the key(same as db column name) value(widget that contains the value) pairs of the 
        for k,v in items.items():
            value = v.getDbInfo()
            #get all column names from keys, separated by a comma
            columns += f"{k},"
            #get all the values, separated by a comma
            values += f"'{value}',"
        #remove comma from both values
        columns = columns[:-1]
        values = values[:-1]
        #conform and return sql
        sql = f'''
            --sql
            INSERT INTO {self.table} ({columns}) VALUES ({values});
            '''
        return sql
    
    def save(self) -> str:
        """Checks if for is dirty - edits have been made -
        - if dirty: checks if there is an id
          - if id: Saves the current selecte1d recod with the information on the form. 
          - else: inserts a new record. 
        - else: 
            shows message in status bar - not saved. 

        Returns:
            str: id of record saved. 
        """
        if self.dirty:
            id_ = self.id_.getDbInfo()
            if id_:
                sql = self.get_sql_update()
                self.db.save(sql, (id_,))
                self.status_bar.showMessage('El registro se actualizó exitosamente', 10000)
                
            else:
                sql = self.get_sql_create_table()
                self.db.execute(sql)
                sql = self.get_sql_new()
                id_ = self.db.save(sql)
                self.id_.populate(id_)
                self.status_bar.showMessage('El registro se creó exitosamente', 10000)
            self.dirty = False
            return id_
        else:
            self.status_bar.showMessage('No se guardó el registro', 1000)

