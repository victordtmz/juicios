from inspect import _void
import sys
import os
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QWidget, QVBoxLayout)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSortFilterProxyModel, QRegularExpression
from globalElements import constants, functions
from globalElements.widgets.widgets import spacer, buttonWidget, labelWidget, standardItem, titleBox, treeView, checkBox
from globalElements.widgets.lineEdits import lineEditFilterGroup
# import mainList



class main(QWidget):
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

    
    def __repr__(self) -> str:
        return '''Main Window => Juicios y Trámites'''
    

    def initUi(self):
        """Main function that calls required functions to initiate the program. 
        """
        self.setWindowTitle('Enlace LLC - Juicios y Trámites')
        self.iconEnlace = QIcon( f'{constants.DB_FILES}\icons\enlace_juicios.png')
        self.setWindowIcon(self.iconEnlace)
        # self.tipo_filters()
        self.config_main_list()
        self.config_layout()
        self.showMaximized()
        self.set_connections()

    def set_connections(self):
        self.tipo_filter_widget.selection_model.selectionChanged.connect(self.apply_filter_tipo)
        self.tipo_filter_widget.activos.toggled.connect(self.activos_toggle)
        self.tipo_filter_widget.inactivos.toggled.connect(self.inactivos_toggle)
        self.tipo_filter_widget.search.txt.textChanged.connect(self.apply_search)
        self.tipo_filter_widget.btn_folder.pressed.connect(self.openFolder)

    def config_main_list(self):
        """Configuration of main list items (Juicios)
        """
        self.list = mainList()
        self.proxy_tipo = QSortFilterProxyModel()
        self.proxy_tipo.setSourceModel(self.list.list.standardModel)
        self.proxy_search = QSortFilterProxyModel()
        self.proxy_search.setSourceModel(self.proxy_tipo)
        self.list.list.setModel(self.proxy_search)




    def config_layout(self):
        """Configuration of the layout of all widets"""
        self.tipo_filter_widget = filtersWidget()
        self.form = form()
        # self.centralWidget_ = QWidget()
        self.layout_ = QHBoxLayout()
        self.layout_.addWidget(self.tipo_filter_widget)
        self.layout_.addWidget(self.list,1)
        self.layout_.addWidget(self.form,1)
        self.setLayout(self.layout_)
        # self.setCentralWidget(self.centralWidget_)

    def apply_filter_tipo(self):
        """When selection changes of case list (civil, administrativo, migratorio, etc), 
        (including removing a selection), it will take the selected item and filter out the juicios list
        to only that categorie.

        If nothing is selected, it will search for empty sting, removing this filter. 
        
        Search column: 0 - this is the column on juicios list.  

        Search type: literal string - Exact match. 

        """
        selection_model = self.tipo_filter_widget.selection_model
        if selection_model.hasSelection():
            text = self.tipo_filter_widget.get_value()
        else: text = ''
        self.proxy_tipo.setFilterFixedString(text)
        self.proxy_tipo.setFilterKeyColumn(0)

    def apply_search(self):
        """When any character is typed or removed, this method will execute, searching for a match. 

        Search column: all columns. 
        
        search type: regular expression. (set to iclude latin or non latin vowels (Á == a))
        """
        value = self.tipo_filter_widget.search.getInfo()
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
                activos = list(map(lambda v: (k,v, 'Activo'), values))
                self.list.add_activos(activos)
        
        #inactivos
        if self.inactivos_checked:
            self.filter_items.update(self.inactivos.keys())
            for k, values in self.inactivos.items():
                inactivos = list(map(lambda v: (k,v, 'Inactivo'), values))
                self.list.add_inactivos(inactivos)

        self.list.list.setColumnHidden(2, True)

        #filter list
        current_value = self.tipo_filter_widget.get_value()
        self.tipo_filter_widget.populate((self.filter_items))
        self.tipo_filter_widget.find_item(current_value)


            
    def activos_toggle(self, checked):
        """If activos is unchecked, inactivos will get checked, to make sure at least
        one fo the items is checked, then it will requery.
        """
        self.activos_checked = checked
        if not self.activos_checked and not self.inactivos_checked:
            self.tipo_filter_widget.inactivos.setChecked(True)
            return
        self.populate()


    def inactivos_toggle(self, checked):
        """If activos is unchecked, inactivos will get checked, to make sure at least
        one fo the items is checked, then it will requery.
        """
        self.inactivos_checked = checked
        if not self.inactivos_checked and not self.activos_checked:
            self.tipo_filter_widget.activos.setChecked(True)
            return
        self.populate()

    def openFolder(self):
        record = self.list.get_values()
        if record:
            if record[2] == 'Activo': root = constants.ROOT_JUICIOS
            else: root = constants.ROOT_JUICIOS_ARCHIVADOS
            folder = f'{root}\{record[0]}\{record[1]}'
            os.startfile(folder)




class mainList(QWidget):
    """main list of items that contains all the cases with their type.
    info is populated on parent widget requery() -> populate() functions. 
    Columns:
        0 => Heading: Tipo; data: case category. 
        0 => Heading: Expediente; data: Client name with short case explanation.

    Args:
        QWidget (_type_): _description_
    """
    def __init__(self):
        super().__init__()
        self.list = treeView()#params fontSize = 13, rowHeight = 42
        self.selection_model = self.list.selectionModel()
        self.list.standardModel.setHorizontalHeaderLabels(['Tipo', 'Expediente'])
        
        self.list.setColumnWidth(0, 140)

        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout_)
        # self.layout_.addWidget(self.activos_filter)
        # self.layout_.addWidget(self.btn_clear)
        self.layout_.addWidget(self.list,1)

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
            list: list of string values selected
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
    



class filtersWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.activos_filter = titleBox()
        spacer_ = spacer('     ', 'h1')
        self.activos = checkBox('Activos', 13, 'h1')
        self.activos.setChecked(True)
        self.inactivos = checkBox('Inactivos', 13, 'h1')
        self.activos_filter.layout_.addWidget(spacer_)
        self.activos_filter.layout_.addWidget(self.activos)
        self.activos_filter.layout_.addWidget(self.inactivos)
        self.search_lbl = labelWidget("Búsqueda:", 14, True)
        self.search = lineEditFilterGroup()
        
        self.btn_folder = buttonWidget('  Abrir carpeta',13, icon=constants.iconOpenFolder)
        self.btn_folder.setFixedHeight(35)
        self.btn_clear = buttonWidget('  Eliminar filtro',13, icon=constants.iconClearFilter)
        self.btn_clear.setFixedHeight(35)
        
        self.list = treeView()
        self.selection_model = self.list.selectionModel()
        self.list.setHeaderHidden(True)

        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout_)
        self.layout_.addWidget(self.activos_filter)
        self.layout_.addWidget(self.btn_folder)
        self.layout_.addWidget(self.search_lbl)
        self.layout_.addWidget(self.search)
        self.layout_.addWidget(self.btn_clear)
        self.layout_.addWidget(self.list,1)

        self.btn_clear.pressed.connect(self.list.clearSelection)
        

    def populate(self, items):
        """removes all current items, adds itemms provided and sorts them (1 column)

        Args:
            items (iterable): list of strings
        """
        self.remove_all_items()
        self.add_items(items)
        self.list.standardModel.sort(0)

    def add_items(self, items):
        """Adds item to filter list.  Calls the local method add_item to make sure the 
        parent method is provided with the correct arg type. 

        Args:
            items (iterable): list of strings
        """
        for i in items:
            self.add_item(i)

    def add_item(self, item):
        """Adds item to type of case filter list

        Args:
            item (string): item is passed to the tree add_item() as tupple (required)
        """
        self.list.add_item((item,))

    def remove_all_items(self):
        """Removes all items from the list. 
        """
        self.list.remove_all_items()

    def get_value(self) -> str:
        """Returns:
            str: the current selected value
        """
        values = self.list.get_values()
        if values:
            return values[0]

    def find_item(self, text):
        model = self.list.standardModel
        no_records= model.rowCount()
        current_row = 0
        while current_row < no_records:
            index = model.index(current_row, 0)
            current_value = model.data(index)
            if current_value == text:
                self.list.setCurrentIndex(index)
            current_row += 1

class form(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(500)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())