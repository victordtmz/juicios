import sys
import os
from PyQt6.QtWidgets import (QApplication,  QHBoxLayout, 
    QWidget, QVBoxLayout, QMainWindow)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSortFilterProxyModel, QRegularExpression
from globalElements import constants, functions
from widgets.widgets import spacer, buttonWidget, labelWidget, standardItem, titleBox, treeView, checkBox, tabWidget
from main_list.main import main as mainList
# import mainList

class main(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.init_ui()
        self.layout_config()

    def init_ui(self):
        self.setWindowTitle('Enlace LLC - Juicios y Trámites')
        self.iconEnlace = QIcon( f'{constants.DB_FILES}\icons\enlace_juicios.png')
        self.setWindowIcon(self.iconEnlace)

    def layout_config(self):
        self.main_list = mainList()
        self.tabWidget = tabWidget("h1")
        self.tabWidget.addTab(self.main_list, 'Main Menu')
        
        self.setCentralWidget(self.tabWidget)
    
    def __repr__(self) -> str:
        return '''Main Window => Juicios y Trámites'''


    




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.showMaximized()
    sys.exit(app.exec())

