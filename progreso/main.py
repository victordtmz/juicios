from cmath import exp
import shutil
import sys
import os
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QWidget, QVBoxLayout, QStatusBar, QMainWindow)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSortFilterProxyModel, QRegularExpression
from globalElements import constants, functions
from widgets import widgets
from widgets.widgets import spacer, buttonWidget, labelWidget, standardItem, titleBox, treeView, checkBox
from widgets.lineEdits import lineEditFilterGroup
from progreso import form, list_

# import mainList



class main(QMainWindow):
    """it takes bot widgets, mainLis and filterList into this widget, populating both lists and 
    adding functionality (filter application, removal, search)

    Args:
        QWidget
    """
    def __init__(self):
      
        super().__init__()
        self.activos = {}
        self.inactivos = {}
        self.activos_checked = True
        self.inactivos_checked = False
        self.filter_items = set([])
        self.expediente = self.form.db.expediente
        
        
        self.initUi()
        self.requery()

        # self.db = db.main()
        # self.db.select_detalles()

    
    def __repr__(self) -> str:
        return '''Main Window => Juicios y Trámites'''
    

    def initUi(self):
        """Main function that calls required functions to initiate the program. 
        """
        self.setWindowTitle('Enlace LLC - Juicios y Trámites')
        self.iconEnlace = QIcon( f'{constants.DB_FILES}\icons\enlace_juicios.png')
        self.setWindowIcon(self.iconEnlace)
        self.status_bar = QStatusBar()
        self.status_bar.setContentsMargins(0,0,0,0)
        self.setStatusBar(self.status_bar)
        # self.tipo_filters()
        self.config_main_list()
        self.config_layout()
        self.showMaximized()
        self.set_connections()

    def set_connections(self):
        # self.filters.selection_model.selectionChanged.connect(self.apply_filter_tipo)
        # self.filters.activos.toggled.connect(self.activos_toggle)
        # self.filters.inactivos.toggled.connect(self.inactivos_toggle)
        # self.filters.search.txt.textChanged.connect(self.apply_search)
        self.list.list.selectionModel().selectionChanged.connect(self.selectionChanged)
        self.form.btn_save.pressed.connect(self.save_detalles)
        self.list.btn_requery.pressed.connect(self.requery)
        # self.list.btn_new.pressed.connect(self.new_item)
        # self.list.btn_delete.pressed.connect(self.delete_window_open)
        # self.list.btn_edit.pressed.connect(self.edit_window_open)


    def config_main_list(self):
        """Configuration of main list items (Juicios)
        """
        self.list = list_.main()
        self.proxy_tipo = QSortFilterProxyModel()
        self.proxy_tipo.setSourceModel(self.list.list.standardModel)
        self.proxy_search = QSortFilterProxyModel()
        self.proxy_search.setSourceModel(self.proxy_tipo)
        self.list.list.setModel(self.proxy_search)




    def config_layout(self):
        """Configuration of the layout of all widets"""
        self.form = form.main()
        self.centralWidget_ = QWidget()
        self.layout_ = QHBoxLayout()
        self.layout_.setContentsMargins(0,0,0,0)
        # self.layout_.addWidget(self.filters)
        self.layout_.addWidget(self.list,1)
        self.layout_.addWidget(self.form,1)
        self.centralWidget_.setLayout(self.layout_)
        self.setCentralWidget(self.centralWidget_)

    def apply_filter_tipo(self):
        """When selection changes of case list (civil, administrativo, migratorio, etc), 
        (including removing a selection), it will take the selected item and filter out the juicios list
        to only that categorie.

        If nothing is selected, it will search for empty sting, removing this filter. 
        
        Search column: 0 - this is the column on juicios list.  

        Search type: literal string - Exact match. 

        """
        selection_model = self.filters.selection_model
        if selection_model.hasSelection():
            text = self.filters.get_value()
        else: text = ''
        self.proxy_tipo.setFilterFixedString(text)
        self.proxy_tipo.setFilterKeyColumn(0)

    def apply_search(self):
        """When any character is typed or removed, this method will execute, searching for a match. 

        Search column: all columns. 
        
        search type: regular expression. (set to iclude latin or non latin vowels (Á == a))
        """
        value = self.filters.search.getInfo()
        value = functions.create_regEx(value)
        value = QRegularExpression(value,QRegularExpression.PatternOption.CaseInsensitiveOption)
        self.proxy_search.setFilterRegularExpression(value)
        self.proxy_search.setFilterKeyColumn(-1)

            

    def requery(self):
        """From: OneDrive/enlace
        Scanns Juicios and places items in self.activos dictionary.
        Scans Juicios_archivados and places items in self.inactivos dictionary. 

        Items: 
            - First pass will collect the folder names and place it as "tipo" (it's the category)
            - Second pass will get the sub-folders and place each as the case to be attended. 
        """
        #obtener all elements from activos
        self.activos.clear()
        for folder in os.scandir(constants.ROOT_JUICIOS):
            if folder.is_dir():
                tipo = folder.name
                for subFolder in os.scandir(folder):
                    if subFolder.is_dir():
                        expediente = subFolder.name
                        if tipo in self.activos:
                            self.activos[tipo].append(expediente)
                        else:
                            self.activos[tipo] = [expediente]

        # Obtener all elements from inactivos
        self.inactivos.clear()
        for folder in os.scandir(constants.ROOT_JUICIOS_ARCHIVADOS):
            if folder.is_dir():
                tipo = folder.name
                for subFolder in os.scandir(folder):
                    if subFolder.is_dir():
                        expediente = subFolder.name
                        if tipo in self.inactivos:
                            self.inactivos[tipo].append(expediente)
                        else:
                            self.inactivos[tipo] = [expediente]
                
        self.populate()
        
    def populate(self):
        """To avoid scannind the directories at every time a search or toggle between activos and inactivos, 
        this function will take the information placed on self.activos and self.inactivos and use to populate 
        the lists on the widget. 
        """
        #filter list
        self.filter_items.clear()
        self.list.remove_all_items()
        
        # Activos
        if self.activos_checked:
            #add items not included in filter items
            self.filter_items.update(self.activos.keys())
            # convert the values of the dict into a tupple with type of juicio
            for k, values in self.activos.items():
                activos = list(map(lambda v: (k,v, 'Juicios'), values))
                self.list.add_activos(activos)
        
        #inactivos
        if self.inactivos_checked:
            self.filter_items.update(self.inactivos.keys())
            for k, values in self.inactivos.items():
                inactivos = list(map(lambda v: (k,v, 'Juicios_archivados'), values))
                self.list.add_inactivos(inactivos)

        self.list.list.setColumnHidden(2, True)

        #filter list


            
    def activos_toggle(self, checked):
        """If activos is unchecked, inactivos will get checked, to make sure at least
        one fo the items is checked, then it will requery.
        """
        self.activos_checked = checked
        if not self.activos_checked and not self.inactivos_checked:
            self.filters.inactivos.setChecked(True)
            return
        self.populate()


    def inactivos_toggle(self, checked):
        """If activos is unchecked, inactivos will get checked, to make sure at least
        one fo the items is checked, then it will requery.
        """
        self.inactivos_checked = checked
        if not self.inactivos_checked and not self.activos_checked:
            self.filters.activos.setChecked(True)
            return
        self.populate()

     

    def selectionChanged(self):
        
        self.save_detalles()
        self.form.db.expediente = self.list.get_values()
        self.form.populate()
        # self.form.expediente = 
        # self.db.connect()
        # detalles = self.db.select_detalles()
        # if detalles:
        #     self.form.populate(detalles)
        # else:
        #     self.form.clear()


    def save_detalles(self):
        self.form.save()
        # if self.form.dirty:
            # detalles = self.form.get_info()
            # msg = self.form.save()
            # self.form.dirty = False
            # self.status_bar.showMessage(f'{msg[0]}', 10000)
            # if msg[1]:
            #     self.form.id_.populate(msg[1])
        

    

        
        

    


    
        






    






if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())