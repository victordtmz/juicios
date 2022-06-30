import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow)
from PyQt6.QtGui import QIcon 
from PyQt6.QtCore import QSortFilterProxyModel
from globalElements import constants
from widgets.widgets import tabWidget, deleteWarningBox
from main_list.main import main as mainList
# from progreso import main as progreso
import detalles
# import mainList 

class main(QMainWindow):
    def __init__(self):  
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Enlace LLC - Juicios y Trámites')
        self.iconEnlace = QIcon( f'{constants.DB_FILES}\icons\enlace_juicios.png')
        self.setWindowIcon(self.iconEnlace)
        self.layout_config() 
        self.set_connections() 

    def layout_config(self):
        self.main_list = mainList()
        self.tabWidget = tabWidget("h1")
        self.tabWidget.addTab(self.main_list, 'Main Menu')
        
        self.setCentralWidget(self.tabWidget)

    def set_connections(self):
        self.main_list.btn_details.pressed.connect(self.open_details)
        self.tabWidget.tab_closed.connect(self.before_tab_closed)

    def open_details(self):
        expediente = self.main_list.list.get_values()
        if expediente:
            # self.progreso.expediente = expediente
            self.details = detalles.main(expediente)
            self.tabWidget.addTab(self.details, expediente[1])
            self.tabWidget.setCurrentWidget(self.details)
        else:
            msg = deleteWarningBox('Seleccione el registro que desea abrir.', 13)   
            msg.exec() 

      
    def __repr__(self) -> str:
        return '''Main Window => Juicios y Trámites'''

    def before_tab_closed(self):
        closed_widget = self.tabWidget.currentWidget()
        if closed_widget == self.details:
            widgets_count = self.details.tabWidget.count()
            self.details.progreso.save_record()
            if widgets_count > 1:
                print('Se cerraron mas de dos widgets a la vez, configurar save para el resto de los widgets')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.showMaximized()
    sys.exit(app.exec())

