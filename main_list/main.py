from cmath import exp
import shutil
import sys
import os
from turtle import Turtle
from typing import Iterable
from urllib import response
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QWidget, QVBoxLayout, QStatusBar, QMainWindow, QGridLayout)
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import QSortFilterProxyModel, QRegularExpression, Qt
from globalElements import constants, functions
from widgets import widgets
from widgets.widgets import spacer, buttonWidget, labelWidget, standardItem, titleBox, treeView, checkBox
from widgets.lineEdits import lineEditFilterGroup
from main_list import filters, form, list_, edit_form, delete_form

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
        self.configure_heading()
        self.config_layout()
        self.showMaximized()
        self.set_connections()

    def set_connections(self):
        self.filters.selection_model.selectionChanged.connect(self.apply_filter_tipo)
        self.filters.activos.toggled.connect(self.activos_toggle)
        self.filters.inactivos.toggled.connect(self.inactivos_toggle)
        self.filters.search.txt.textChanged.connect(self.apply_search)
        self.list.list.selectionModel().selectionChanged.connect(self.selectionChanged)
        self.form.btn_save.pressed.connect(self.save_detalles)
        self.btn_requery.pressed.connect(self.requery)
        self.btn_new.pressed.connect(self.new_item)
        self.btn_delete.pressed.connect(self.delete_window_open)
        self.btn_edit.pressed.connect(self.edit_window_open)
        self.btn_folder.pressed.connect(self.open_folder)
        # self.btn_details.pressed.connect(self.open_details)


    def configure_heading(self): 
        self.heading = QWidget()
        self.heading_layout = QHBoxLayout()
        # self.heading_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.heading_layout.setContentsMargins(0,0,0,0)
        self.heading_layout.setSpacing(0)
        self.heading.setLayout(self.heading_layout)

        self.btn_folder = buttonWidget('  Abrir carpeta',13, icon=constants.iconOpenFolder)
        self.btn_requery = buttonWidget('  Refresh', 13, constants.iconRefresh)
        self.btn_new = buttonWidget('   Nuevo', 13, constants.iconNew)
        self.btn_delete = buttonWidget('  Eliminar', 13, constants.iconDelete)
        self.btn_edit = buttonWidget(' Editar', 13)
        self.btn_details = buttonWidget('  Detalles', 13, constants.iconFilter)
        self.spacer = buttonWidget()
        cursor = QCursor(Qt.CursorShape.ArrowCursor)
        self.spacer.setCursor(cursor)
        # self.spacer.setMinimumWidth(500)

        self.heading_layout.addWidget(self.btn_requery)
        self.heading_layout.addWidget(self.btn_folder)
        self.heading_layout.addWidget(self.btn_new)
        self.heading_layout.addWidget(self.btn_delete)
        self.heading_layout.addWidget(self.btn_edit)
        self.heading_layout.addWidget(self.btn_details)
        self.heading_layout.addWidget(self.spacer,1)
        # self.heading_layout.setAlignment(self.spacer, Qt.AlignmentFlag.AlignRight)

        # self.heading_layout.addWidget(self.btn_requery)
        # self.heading_layout.addWidget(self.btn_folder)
        # self.heading_layout.addWidget(self.btn_new)
        # self.heading_layout.addWidget(self.btn_delete)
        # self.heading_layout.addWidget(self.btn_edit)


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
        self.filters = filters.main()
        self.form = form.main()
        self.centralWidget_ = QWidget()
        self.layout_ = QGridLayout()
        self.layout_.setContentsMargins(0,0,0,0)
        self.layout_.addWidget(self.filters,0,0,2,1, Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.heading,0,1,1,2)
        self.layout_.addWidget(self.list,1,1)
        self.layout_.addWidget(self.form,1,2)
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
        current_value = self.filters.get_value()
        self.filters.populate((self.filter_items))
        self.filters.find_item(current_value)


            
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
        
    def open_folder(self):
        self.list.open_folder()

    def new_item(self):
        self.edit_form = edit_form.main()
        self.edit_form.activo.populate('Juicios')
        items = list(self.filter_items)
        self.edit_form.setWindowTitle('Agregar nuevo elemento')
        items.insert(0,"")
        self.edit_form.tipo.addItems(items)
        self.edit_form.btn_save.pressed.connect(self.save_new)

        self.edit_form.exec()

    def save_new(self):
        info = self.edit_form.get_info()
        
        tipo_path = f'{constants.ROOT_ENLACE}\{info["activo"]}\{info["tipo"]}'
        folder_path = f'{tipo_path}\{info["expediente"]}'
        #validate record
        errors_ = []
        validation_text = 'Se encontraron los siguientes errores: \n'
        exists_ = os.path.isdir(folder_path)
        if exists_ and info['expediente']:
            errors_.append('  - No se puede crear el registro con esos datos, el registro ya existe')
        if not info['tipo']:
            errors_.append('  - Debe proporcionar el tipo de expediente')
        if not info['expediente']:
            errors_.append('  - Debe proporcionar el nombre de expediente')
        if errors_:
            for i in errors_:
                validation_text += i
                validation_text += '\n'
            validation_text += 'Corrija los errores e intente nuevamente'
            self.edit_form.validate.setText(validation_text)
            return
            
            
        if not os.path.isdir(tipo_path):
            os.mkdir(tipo_path)
        os.mkdir(folder_path)
        self.edit_form.deleteLater()
        self.requery()
        self.find_select_item_removing_filters([info["tipo"], info["expediente"], info["activo"]])
        # self.list.find_item(expediente)
        #find item
        # self.remove_all_filters()
        


    def find_select_item_removing_filters(self, expediente:list):
        index = self.find_item(expediente)
        if index:
            self.list.list.setCurrentIndex(index)
        else:
            self.filters.list.clearSelection()
            index = self.find_item(expediente)
            if index:
                self.list.list.setCurrentIndex(index)
            else:
                self.filters.search.txt.clear()
                index = self.find_item(expediente)
                if index:
                    self.list.list.setCurrentIndex(index)
                else: 
                    self.filters.activos.setChecked(True)
                    self.filters.inactivos.setChecked(True)
                    index = self.find_item(expediente)
                    if index:
                        self.list.list.setCurrentIndex(index)


    def find_item(self, expediente:list):
        model = self.proxy_search
        no_records= model.rowCount()
        current_row = 0
        while current_row < no_records:
            indexes = (model.index(current_row, 0),model.index(current_row, 1),model.index(current_row, 2))
            current_values = list(map(lambda x: model.data(x),indexes))
            if current_values == expediente:
                return indexes[0]
            current_row += 1
    
    def delete_window_open(self):
        folder = self.list.get_file_path()
        if folder:
            self.delete_warning_box = delete_form.main()
            self.delete_warning_box.btn_delete.pressed.connect(lambda: self.delete_item(folder))
            self.delete_warning_box.exec()

        else:
            msg = widgets.deleteWarningBox('Seleccione el registro que desea eliminar.', 13)   
            msg.exec()         
            
            # self.list.list.clearSelection()
            # self.db.connection.close()
            # shutil.rmtree(folder)
            # self.requery() 

    def delete_item(self, folder):
        pwd = self.delete_warning_box.pwd.getInfo()
        if pwd == '202020':
            self.delete_warning_box.deleteLater()
            self.list.list.clearSelection()
            self.form.db.connection.close()
            shutil.rmtree(folder)
            self.requery()
            self.status_bar.showMessage(f'Se ha eliminado el registro siguente:   {folder}', 4000)
        else:
            wrong_password_message = labelWidget('Contraseña erronea', 13,False,'red')
            self.delete_warning_box.layout_.insertRow(1, wrong_password_message)

    def edit_window_open(self):
        current_info = self.list.get_values()
        if current_info:
        #prepare form
            self.edit_form = edit_form.main()
            items = list(self.filter_items)
            self.edit_form.setWindowTitle('Editar el elemento seleccionado')
            items.insert(0,"")
            self.edit_form.tipo.addItems(items)
            #populate form. 
            
            self.edit_form.tipo.populate(current_info[0])
            self.edit_form.expediente.populate(current_info[1])
            self.edit_form.activo.populate(current_info[2])
            self.edit_form.btn_save.pressed.connect(lambda: self.save_edit(current_info))

            self.edit_form.exec()
        else:
            msg = widgets.deleteWarningBox('Seleccione el registro que desea editar.', 13)   
            msg.exec()  

    def save_edit(self, current_info):
        tipo = self.edit_form.tipo.getInfo()
        expediente = self.edit_form.expediente.getInfo()
        activo = self.edit_form.activo.getInfo()
        if tipo.strip() != current_info[0].strip() or expediente.strip() != current_info[1].strip():
            current_path = f'{constants.ROOT_ENLACE}\{current_info[2]}\{current_info[0]}\{current_info[1]}'
            new_path = f'{constants.ROOT_ENLACE}\{activo}\{tipo}\{expediente}'
            self.list.list.clearSelection()
            self.form.db.connection.close()
            try:
                shutil.move(current_path, new_path)
            except:
                self.status_bar.showMessage(f'Se produjo un error, verifica archivos y termina el proceso manualmente:   {new_path}', 10000)
            self.requery()
            self.remove_all_filters()
            # self.find_item([tipo, expediente, activo])
            self.find_select_item_removing_filters([tipo, expediente, activo])
            self.status_bar.showMessage(f'Se ha movido el registro a:   {new_path}', 4000)
        else: 
            self.status_bar.showMessage(f'No se ha movido el registro, los datos proporcinados son los mismos')
        self.edit_form.deleteLater()

    def remove_all_filters(self):
        self.filters.remove_all_filters()

    # def open_details(self):
    #     pass

        
        

    


    
        






    






if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())