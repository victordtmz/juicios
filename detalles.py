import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout)
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
from globalElements import constants, functions
from widgets import widgets
from widgets.widgets import spacer, buttonWidget, labelWidget, standardItem, titleBox, treeView, checkBox, tabWidget, okWarningBox
from main_list.main import main as mainList
from progreso import main as progreso
from main_list import form as detalles
# import mainList

class main(QMainWindow):
    def __init__(self, expediente):  
        super().__init__()
        self.expediente = expediente
        self.init_ui()

    def init_ui(self):
        self.layout_config() 
        self.set_connections() 

    def layout_config(self):
        #configure central widget and layout
        self.centralWidget_ = QWidget()
        self.centralWidget_layout = QVBoxLayout()
        self.centralWidget_layout.setContentsMargins(0,0,0,0)
        self.centralWidget_layout.setSpacing(0)
        self.centralWidget_.setLayout(self.centralWidget_layout)
        self.setCentralWidget(self.centralWidget_)
        
        #Configure progreso (main widget)
        self.progreso = progreso.main(self.expediente)
        self.tabWidget = tabWidget("h2")
        self.tabWidget.addTab(self.progreso, '   Progreso   ')

        #Add items to main widget layout
        self.configure_heading()
        self.centralWidget_layout.addWidget(self.heading)
        self.centralWidget_layout.addWidget(self.tabWidget)
        

    def set_connections(self):
        self.btn_folder.pressed.connect(self.open_folder)
        self.btn_details.pressed.connect(self.open_details)
        self.tabWidget.tab_closed.connect(self.before_tab_closed)
    
    def open_details(self):
        self.details = detalles.main(self.progreso.db)
        self.details.expediente = self.expediente
        self.details.table = 'detalles'
        self.details.populate()
        self.tabWidget.addTab(self.details, '  Detalles del caso  ')
        self.tabWidget.setCurrentWidget(self.details)
        self.details.btn_save.pressed.connect(self.details.save)
        self.details.btn_cancel.pressed.connect(self.cancel_details)
        
    def configure_heading(self): 
        self.heading = QWidget()
        self.heading_layout = QHBoxLayout()
        self.heading_layout.setContentsMargins(0,0,0,0)
        self.heading_layout.setSpacing(0)
        self.heading.setLayout(self.heading_layout)

        self.btn_details = buttonWidget('  Ver detalles',13, icon=constants.iconDocOpen)
        self.btn_folder = buttonWidget('  Abrir carpeta',13, icon=constants.iconOpenFolder)

        self.spacer = buttonWidget()
        cursor = QCursor(Qt.CursorShape.ArrowCursor)
        self.spacer.setCursor(cursor)
        # self.spacer.setMinimumWidth(500)

        self.heading_layout.addWidget(self.btn_details)
        self.heading_layout.addWidget(self.btn_folder)
        self.heading_layout.addWidget(self.spacer,1)

    
    def open_folder(self):
        self.progreso.files_tree.folderOpen()

    def cancel_details(self):
        self.details.populate()

    def __repr__(self) -> str:
        return '''Main Window => Juicios y Trámites'''

    def before_tab_closed(self):
        closed_widget = self.tabWidget.currentWidget()
        if closed_widget == self.details:
            self.details.save()
        
    def before_closing(self):
        tabs = self.tabWidget.count()
        index = 0
        while index < tabs:
            self.tabWidget.widget(index).before_closing()
            index += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.showMaximized()
    sys.exit(app.exec())

