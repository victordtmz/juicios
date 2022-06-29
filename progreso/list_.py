import sys
import os
import shutil
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout)
from widgets.treeviews import treeView
from widgets.widgets import buttonWidget
from globalElements import constants
from main_list import edit_form

class main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.set_connections()
        
    def set_connections(self):
        self.btn_folder.pressed.connect(self.open_folder)

    def initUi(self):
        self.configure_list()
        self.configure_heading()
        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout_)
        self.layout_.addWidget(self.heading)

        self.layout_.addWidget(self.list,1)


    def configure_heading(self):
        self.heading = QWidget()
        self.heading_layout = QHBoxLayout()
        self.heading_layout.setContentsMargins(0,0,0,0)
        self.heading_layout.setSpacing(0)
        self.heading.setLayout(self.heading_layout)

        self.btn_folder = buttonWidget('  Abrir carpeta',13, icon=constants.iconOpenFolder)
        self.btn_requery = buttonWidget('  Refresh', 13, constants.iconRefresh)
        self.btn_new = buttonWidget('   Nuevo', 13, constants.iconNew)
        self.btn_delete = buttonWidget('  Eliminar', 13, constants.iconDelete)
        self.btn_edit = buttonWidget(' Editar', 13)

        self.heading_layout.addWidget(self.btn_requery)
        self.heading_layout.addWidget(self.btn_folder)
        self.heading_layout.addWidget(self.btn_new)
        self.heading_layout.addWidget(self.btn_delete)
        self.heading_layout.addWidget(self.btn_edit)

            

    def configure_list(self):
        self.list = treeView()#params fontSize = 13, rowHeight = 42
        # self.list.standardModel.edit
        self.selection_model = self.list.selectionModel()
        self.list.standardModel.setHorizontalHeaderLabels(['Tipo', 'Expediente'])
        
        self.list.setColumnWidth(0, 140)

        

    def add_item(self, item):
        """appends given item to end-bottom of the list

        Args:
            item (string): 
        """
        self.list.add_item(item)

    def remove_all_items(self):
        """Gets the total number of items to clear the list
        """
        self.list.remove_all_items()

    def get_values(self)->list:
        """Gets the values for the selected record

        Returns:
            list: list of string values selected ()
            0 => Tipo; data: case category. 
            1 => Expediente; data: Client name with short case explanation.
            2 => Activos; data: Actio or inactivo - for loading.
        """
        return self.list.get_values()

    def add_activos(self, items):
        """Adds record with font and row height defined on tree.

        Args:
            items (iterable): List of lists, tupple or set of iterable items (records)
        """
        self.list.add_items(items)

    def add_inactivos(self, items):
        """Adds items to list with a dark red color

        Args:
            items (iterable): List of lists, tupple or set of iterable items (records)
        """
        self.list.add_items(items, 'dark red')

    def get_file_path(self):
        record = self.list.get_values()
        if record:
            folder = f'{constants.ROOT_ENLACE}\{record[2]}\{record[0]}\{record[1]}'
            return folder
    
    def open_folder(self):
        folder = self.get_file_path() 
        if folder:
            os.startfile(folder)

   
    
    # def delete(self):
        
    #     folder = self.get_file_path()
    #     if folder:
    #         # os.chmod(folder, 0o777)
    #         # os.rmdir(folder)
    #         self.list.clearSelection()
    #         shutil.rmtree(folder)

    # def find_item(self, text):
    #     model = self.proxym
    #     no_records= model.rowCount()
    #     current_row = 0
    #     while current_row < no_records:
    #         index = model.index(current_row, 1)
    #         current_value = model.data(index)
    #         if current_value == text:
    #             self.list.setCurrentIndex(index)
    #             break
    #         current_row += 1

   
        # sys.exit(app.exec())