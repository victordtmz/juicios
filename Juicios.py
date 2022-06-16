from statistics import mode
import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QToolBar, QPushButton, QHBoxLayout, QLabel,
    QWidget, QVBoxLayout, QListWidget, QTreeView)
from PyQt6.QtGui import QIcon, QAction, QFont, QPixmap
from PyQt6.QtCore import Qt, QSize, QSortFilterProxyModel
from globalElements import constants
from globalElements.widgets import spacer, buttonWidget, labelWidget, titleBox, treeView, checkBox
# import mainList



class main(QMainWindow):
    """

    Args:
        QMainWindow (QtWidgget): QtWidget item
    """
    def __init__(self):
        super().__init__()
        
        
        self.initUi()
        self.requery()

    
    def __repr__(self) -> str:
        return '''Main Window => Juicios y Trámites'''
    
    def set_connections(self):
        self.tipo_filter_widget.selection_model.selectionChanged.connect(self.apply_filter_tipo)
        self.tipo_filter_widget.activos.toggled.connect(self.activos_toggle)
        self.tipo_filter_widget.inactivos.toggled.connect(self.inactivos_toggle)
        

    def initUi(self):
        self.setWindowTitle('Enlace LLC - Juicios y Trámites')
        self.iconEnlace = QIcon( f'{constants.DB_FILES}\icons\enlace_juicios.png')
        self.setWindowIcon(self.iconEnlace)
        self.tipo_filters()
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
        self.centralWidget_ = QWidget()
        self.layout_ = QHBoxLayout()
        self.layout_.addWidget(self.tipo_filter_widget)
        self.layout_.addWidget(self.main_list,1)
        self.centralWidget_.setLayout(self.layout_)
        self.setCentralWidget(self.centralWidget_)

    def tipo_filters(self):
        pass
    
    def apply_filter_tipo(self):
        selection_model = self.tipo_filter_widget.selection_model
        if selection_model.hasSelection():
            text = self.tipo_filter_widget.get_value()
        else: text = ''
        self.proxy_tipo.setFilterFixedString(text)
        self.proxy_tipo.setFilterKeyColumn(0)
            

    def requery(self):
        items = {}
        tipo_filter_value = self.tipo_filter_widget.get_value()
        
        #obtener all elements from activos
        if self.tipo_filter_widget.activos.isChecked():
            for folder in os.scandir(constants.ROOT_JUICIOS):
                if folder.is_dir():
                    tipo = folder.name
                    for subFolder in os.scandir(folder):
                        if subFolder.is_dir():
                            expediente = subFolder.name
                            if tipo in items:
                                items[tipo].append(expediente)
                            else:
                                items[tipo] = [expediente]

        # Obtener all elements from inactivos
        if self.tipo_filter_widget.inactivos.isChecked():
            for folder in os.scandir(constants.ROOT_JUICIOS_ARCHIVADOS):
                if folder.is_dir():
                    tipo = folder.name
                    for subFolder in os.scandir(folder):
                        if subFolder.is_dir():
                            expediente = subFolder.name
                            if tipo in items:
                                items[tipo].append(expediente)
                            else:
                                items[tipo] = [expediente]
        #filter items
        self.tipo_filter_widget.remove_all_items()
        # items = self.tipo_filter_widget.list.standardModel.rowCount()
        self.tipo_filter_widget.add_items(items.keys())
        if tipo_filter_value:
            self.tipo_filter_widget.find_item(tipo_filter_value)
        # for k in sorted(items.keys()):
        #     self.tipo_filter_widget.add_item(k)

        #Main list
        self.main_list.remove_all_items()
        for k,values in sorted(items.items()):
            for v in values:
                record = (k,v)
                self.main_list.add_item(record)
    
    def activos_toggle(self):
        """If activos is unchecked, inactivos will get checked, to make sure at least
        one fo the items is checked, then it will requery.
        """
        if not self.tipo_filter_widget.activos.isChecked():
            if not self.tipo_filter_widget.inactivos.isChecked():
                self.tipo_filter_widget.inactivos.setChecked(True)
                return
        self.requery()

    def inactivos_toggle(self):
        """If activos is unchecked, inactivos will get checked, to make sure at least
        one fo the items is checked, then it will requery.
        """
        if not self.tipo_filter_widget.inactivos.isChecked():
            if not self.tipo_filter_widget.activos.isChecked():
                self.tipo_filter_widget.activos.setChecked(True)
                return
        self.requery()


    
            



   
        
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

        self.btn_clear = buttonWidget('  Eliminar filtros',13, icon=constants.iconClearFilter)
        
        self.list = treeView()
        self.selection_model = self.list.selectionModel()
        self.list.setHeaderHidden(True)

        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout_)
        self.layout_.addWidget(self.activos_filter)
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