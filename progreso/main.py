from cmath import exp
import shutil
import sys
import os
from PyQt6.QtWidgets import (QGridLayout,QApplication, QHBoxLayout, QWidget, QVBoxLayout, QStatusBar, QMainWindow)
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import QSortFilterProxyModel, QRegularExpression, Qt
from globalElements import constants, functions
from widgets import widgets
from widgets.widgets import spacer, buttonWidget, labelWidget, standardItem, titleBox, treeView, checkBox
from widgets.lineEdits import lineEditFilterGroup
from progreso import form, list_
from globalElements import db
from widgets.filesTree import filesTree

# import mainList



class main(QMainWindow):
    def __init__(self, expediente):
      
        super().__init__()
        self.expediente = expediente
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
        self.status_bar = QStatusBar()
        self.status_bar.setContentsMargins(0,0,0,0)
        self.setStatusBar(self.status_bar)
        # self.tipo_filters()
        # self.config_main_list()
        self.configure_heading()
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
        self.btn_requery.pressed.connect(self.requery)
        # self.list.btn_new.pressed.connect(self.new_item)
        # self.list.btn_delete.pressed.connect(self.delete_window_open)
        # self.list.btn_edit.pressed.connect(self.edit_window_open)


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
        self.spacer = buttonWidget()
        cursor = QCursor(Qt.CursorShape.ArrowCursor)
        self.spacer.setCursor(cursor)
        # self.spacer.setMinimumWidth(500)

        self.heading_layout.addWidget(self.btn_requery)
        self.heading_layout.addWidget(self.btn_folder)
        self.heading_layout.addWidget(self.btn_new)
        self.heading_layout.addWidget(self.btn_delete)
        self.heading_layout.addWidget(self.spacer,1)
        




    def config_layout(self):
        """Configuration of the layout of all widets"""
        #init files window
        self.files_tree = filesTree()
        self.files_tree.setLineEditFileBox(13)
        self.files_tree.txtFilePath.setText(f'{constants.ROOT_ENLACE}\{self.expediente[2]}\{self.expediente[0]}\{self.expediente[1]}')
        
        #init Form
        self.db = db.main()
        self.db.expediente = self.expediente
        self.form = form.main(self.db)
        self.form.file_ = self.files_tree.layoutLineEditFileBox
        self.form.lineEditItems = self.files_tree.lineEditItems
        
        self.form.initiate_super()
        # init list

        self.list = list_.main(self.db)



        self.centralWidget_ = QWidget()
        self.layout_ = QGridLayout()
        self.layout_.setContentsMargins(0,0,0,0)
        # self.layout_.addWidget(self.filters)
        self.layout_.addWidget(self.heading,0,0,1,3)
        self.layout_.addWidget(self.list,1,0)
        self.layout_.addWidget(self.form,1,1)
        self.layout_.addWidget(self.files_tree,1,2)
        self.centralWidget_.setLayout(self.layout_)
        self.setCentralWidget(self.centralWidget_)


    def requery(self):
        self.list.requery()
        #obtener all elements from activos
        # sql = '''
        # --sql
        # SELECT id, 
        #     date_ AS 'Fecha',
        #     title AS 'Titulo', 
        #     description_ AS 'Descripcion', 
        #     file_ AS 'Archivo'
        # FROM registros;
        # '''
        
        # records, labels = self.db.select_dict_labels(sql)
        # self.list.remove_all_items()
        # for i in records:
        #     self.list.add_item(i)
        
        # self.list.list.standardModel.setHorizontalHeaderLabels(labels)
        
        # self.list.list.setColumnHidden(0, True)
        # self.list.list.setColumnHidden(3, True)
        # self.list.list.setColumnHidden(4, True)
        # self.list.proxy_search

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
        # prev_id = self.form.save() 
        # if prev_id:
        #     curr_id = self.list.get_id()
        #     self.requery()
        #     self.list.select_record_id(curr_id)
        # else:
        #     # self.form.db.expediente = self.list.get_values()
        #     values = self.list.get_values_dict()
        #     self.form.populate(values)
        # self.form.expediente = self.requeryd
        # self.db.connect()
        # detalles = self.db.select_detalles()
        # if detalles:
        #     self.form.populate(detalles)
        # else:
        #     self.form.clear()


    def save_detalles(self):
        prev_id = self.form.save() 
        if prev_id:
            curr_id = self.list.get_id()
            self.requery()
            self.list.select_record_id(curr_id)
        else:
            # self.form.db.expediente = self.list.get_values()
            values = self.list.get_values_dict()
            self.form.populate(values)
        # if self.form.dirty:
            # detalles = self.form.get_info()
            # msg = self.form.save()
            # self.form.dirty = False
            # self.status_bar.showMessage(f'{msg[0]}', 10000)
            # if msg[1]:
            #     self.form.id_.populate(msg[1])

    # def configure_form(self):
    #     self.db = db.main()
    #     self.form = form.main('registros' ,self.db)
        

    

        
        

    


    
        






    






if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())