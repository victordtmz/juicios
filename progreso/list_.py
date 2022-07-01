from ast import Try
import sys
import os
import shutil
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout)
from PyQt6.QtCore import QSortFilterProxyModel, QRegularExpression, Qt

from widgets.treeviews import treeView
from widgets.widgets import buttonWidget, labelWidget
from globalElements import constants, functions
from main_list import edit_form
from widgets.lineEdits import lineEditFilterGroup

class main(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.initUi()
        self.set_connections()
        
    def set_connections(self):
        # self.btn_folder.pressed.connect(self.open_folder)
        self.search.txt.textChanged.connect(self.apply_search)

    def initUi(self):
        self.configure_list()
        # self.configure_heading()
        self.layout_ = QFormLayout()
        self.layout_.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout_)
        # self.layout_.addRow(self.heading)
        self.layout_.addRow(labelWidget('Búsqueda:', 13, True, 'blue') , self.search)
        self.layout_.addRow(self.list)

    def requery(self):
        #obtener all elements from activos
        sql = '''
        --sql
        SELECT id, 
            date_ AS 'Fecha',
            title AS 'Titulo', 
            description_ AS 'Descripcion', 
            file_ AS 'Archivo'
        FROM registros;
        '''
        try: records, labels = self.db.select_dict_labels(sql)
        except: return
            
        self.list.remove_all_items()
        for i in records:
            self.add_item(i)
        
        self.list.standardModel.setHorizontalHeaderLabels(labels)
        
        self.list.setColumnHidden(0, True)
        self.list.setColumnHidden(3, True)
        self.list.setColumnHidden(4, True)
        self.proxy_search.sort(1, Qt.SortOrder.DescendingOrder)
        
    def configure_list(self):
        self.list = treeView()#params fontSize = 13, rowHeight = 42
        self.list.setSortingEnabled(True)
        # self.list.standardModel.edit
        self.selection_model = self.list.selectionModel()

        self.search = lineEditFilterGroup()
        self.search.setMaximumWidth(400)

        
        self.list.setColumnWidth(0, 140)
        
        self.proxy_search = QSortFilterProxyModel()
        self.proxy_search.setSourceModel(self.list.standardModel)
        self.list.setModel(self.proxy_search)

    def apply_search(self):
        """When any character is typed or removed, this method will execute, searching for a match. 

        Search column: all columns. 
        
        search type: regular expression. (set to iclude latin or non latin vowels (Á == a))
        """
        value = self.search.getInfo()
        value = functions.create_regEx(value)
        value = QRegularExpression(value,QRegularExpression.PatternOption.CaseInsensitiveOption)
        self.proxy_search.setFilterRegularExpression(value)
        self.proxy_search.setFilterKeyColumn(-1)
        self.proxy_search.sort(1, Qt.SortOrder.DescendingOrder)

    def add_item(self, item):
        """appends given item to end-bottom of the list

        Args:
            item (list): 
        """
        self.list.add_item(item)

    def remove_all_items(self):
        """Gets the total number of items to clear the list
        """
        self.list.remove_all_items()

    def get_id(self) -> str:
        record = self.list.get_row_values()
        if record:
            return record[0]

    def get_row_values(self)->list:
        """Gets the values for the selected record
        Returns:
            list: list of string values selected ()
            0 => Tipo; data: case category. 
            1 => Expediente; data: Client name with short case explanation.
            2 => Activos; data: Actio or inactivo - for loading.
        """
        values = self.list.get_row_values() 
        return values
    
    def get_row_db_values_dict(self)->dict:
        """Gets the values for the selected record
        Returns:
            dict: Dictionary with same key value as headers in table. 
        """
        values = self.list.get_row_values() 
        if values:
        
            values_dict = {}
            values_dict['id'] = values[0]
            values_dict['date_'] = values[1]
            values_dict['title'] = values[2]
            values_dict['description_'] = values[3]
            values_dict['file_'] = values[4]
            return values_dict

    def get_row_values_dict(self):
        """
        Returns:
            dict: Dictionary with row values with headers as keys
        """
        return self.list.get_row_values_dict()

    def select_record_by_id(self, id_):
        """Will search for a record with the given id and select it if found.
        Args:
            id_ (str): record id 
        """
        model = self.proxy_search
        no_records= model.rowCount()
        current_row = 0
        while current_row < no_records:
            index = model.index(current_row, 0)
            current_value = model.data(index)
            if current_value == id_:
                self.list.setCurrentIndex(index)
                break
            current_row += 1

