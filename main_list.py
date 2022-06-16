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
    """

    Args:
        QMainWindow (QtWidgget): QtWidget item
    """
    def __init__(self):
        super().__init__()
        self.activos = {}
        self.inactivos = {}
        self.activos_checked = True
        self.inactivos_checked = False
        
        
        self.initUi()
        self.requery()

    
    def __repr__(self) -> str:
        return '''Main Window => Juicios y Trámites'''
    
    def set_connections(self):
        self.tipo_filter_widget.selection_model.selectionChanged.connect(self.apply_filter_tipo)
        self.tipo_filter_widget.activos.toggled.connect(self.activos_toggle)
        self.tipo_filter_widget.inactivos.toggled.connect(self.inactivos_toggle)
        self.tipo_filter_widget.search.txt.textChanged.connect(self.apply_search)
        

    def initUi(self):
        self.setWindowTitle('Enlace LLC - Juicios y Trámites')
        self.iconEnlace = QIcon( f'{constants.DB_FILES}\icons\enlace_juicios.png')
        self.setWindowIcon(self.iconEnlace)
        # self.tipo_filters()
        self.config_main_list()
        self.config_layout()
        self.showMaximized()
        self.set_connections()

    def config_main_list(self):
        self.main_list = mainList()
        self.proxy_tipo = QSortFilterProxyModel()
        self.proxy_tipo.setSourceModel(self.main_list.list.standardModel)
        self.proxy_search = QSortFilterProxyModel()
        self.proxy_search.setSourceModel(self.proxy_tipo)
        self.main_list.list.setModel(self.proxy_search)




    def config_layout(self):
        
        self.tipo_filter_widget = tipoFilter()
        # self.centralWidget_ = QWidget()
        self.layout_ = QHBoxLayout()
        self.layout_.addWidget(self.tipo_filter_widget)
        self.layout_.addWidget(self.main_list,1)
        self.setLayout(self.layout_)
        # self.setCentralWidget(self.centralWidget_)

    def apply_filter_tipo(self):
        selection_model = self.tipo_filter_widget.selection_model
        if selection_model.hasSelection():
            text = self.tipo_filter_widget.get_value()
        else: text = ''
        self.proxy_tipo.setFilterFixedString(text)
        self.proxy_tipo.setFilterKeyColumn(0)

    def apply_search(self):
        value = self.tipo_filter_widget.search.getInfo()
        value = functions.create_regEx(value)
        value = QRegularExpression(value,QRegularExpression.PatternOption.CaseInsensitiveOption)
        self.proxy_search.setFilterRegularExpression(value)
        self.proxy_search.setFilterKeyColumn(-1)

            

    def requery(self):
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
        #filter list
        filter_items = set([])
        # Expedientes ------------------
        self.main_list.remove_all_items()
        
        # Activos
        if self.activos_checked:
            for k, v in self.activos.items():
                #filter list
                filter_items.add(k)
                for i in v:
                    tipo = standardItem(k,13,45)
                    expediente = standardItem(i,13,45)
                    self.main_list.list.rootNode.appendRow((tipo, expediente))
        #inactivos
        if self.inactivos_checked:
            for k, v in self.inactivos.items():
                #filter list
                filter_items.add(k)
                for i in v:
                    tipo = standardItem(k,13,45, 'dark red')
                    expediente = standardItem(i,13,45, 'dark red')
                    self.main_list.list.rootNode.appendRow((tipo, expediente))
        #filter list
        current_value = self.tipo_filter_widget.get_value()
        self.tipo_filter_widget.remove_all_items()
        
        for i in sorted(filter_items):
            value = standardItem(i, 13, 45)
            self.tipo_filter_widget.list.rootNode.appendRow((value,))
        
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

        
        # if not self.tipo_filter_widget.activos.isChecked():
        #     if not self.tipo_filter_widget.inactivos.isChecked():
        #         self.tipo_filter_widget.inactivos.setChecked(True)
        #         return
        # self.requery()

    def inactivos_toggle(self, checked):
        """If activos is unchecked, inactivos will get checked, to make sure at least
        one fo the items is checked, then it will requery.
        """
        self.inactivos_checked = checked
        if not self.inactivos_checked and not self.activos_checked:
            self.tipo_filter_widget.activos.setChecked(True)
            return
        self.populate()


    
            



   
        
class mainList(QWidget):
    def __init__(self):
        super().__init__()
        self.list = treeView()
        self.selection_model = self.list.selectionModel()
        self.list.standardModel.setHorizontalHeaderLabels(['Tipo', 'Expediente'])
        self.list.setColumnWidth(0, 140)

        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout_)
        # self.layout_.addWidget(self.activos_filter)
        # self.layout_.addWidget(self.btn_clear)
        self.layout_.addWidget(self.list,1)

    def add_items(self, items):
        self.list.add_items(items)

    def add_item(self, item):
        self.list.add_item(item)

    def remove_all_items(self):
        self.list.remove_all_items()

    def get_values(self):
        index = self.selection_model.selectedIndexes()
        values = (index[0].data(), index[1].data())
        return values

    



class tipoFilter(QWidget):
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

        self.btn_clear = buttonWidget('  Eliminar tipo',13, icon=constants.iconClearFilter)
        self.btn_clear.setFixedHeight(35)
        
        self.list = treeView()
        self.selection_model = self.list.selectionModel()
        self.list.setHeaderHidden(True)

        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout_)
        self.layout_.addWidget(self.activos_filter)
        self.layout_.addWidget(self.search_lbl)
        self.layout_.addWidget(self.search)
        self.layout_.addWidget(self.btn_clear)
        self.layout_.addWidget(self.list,1)

        self.btn_clear.pressed.connect(self.list.clearSelection)
        

    def add_items(self, items):
        self.list.add_items(items)

    def add_item(self, item):
        self.list.add_item(item)

    def remove_all_items(self):
        self.list.remove_all_items()

    def get_value(self):
        return self.selection_model.currentIndex().data()

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





if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())

    # print('This is the name of the script: ', sys.argv[0])

    # print(len(sys.argv))
    # print(str(sys.argv))