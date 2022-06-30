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
        self.list.list.selectionModel().selectionChanged.connect(self.selectionChanged)
        self.form.btn_save.pressed.connect(self.save_record)
        self.form.btn_cancel.pressed.connect(self.cancel_form_edit)
        self.btn_requery.pressed.connect(self.requery)
        self.btn_new.pressed.connect(self.new_record)
        self.btn_delete.pressed.connect(self.delete_record)



    def configure_heading(self): 
        self.heading = QWidget()
        self.heading_layout = QHBoxLayout()
        self.heading_layout.setContentsMargins(0,0,0,0)
        self.heading_layout.setSpacing(0)
        self.heading.setLayout(self.heading_layout)

        self.btn_requery = buttonWidget('  Refresh', 13, constants.iconRefresh,size='h2')
        self.btn_new = buttonWidget('   Nuevo', 13, constants.iconNew, size='h2')
        self.btn_delete = buttonWidget('  Eliminar', 13, constants.iconDelete, size='h2')

        self.spacer = buttonWidget(size='h2')
        cursor = QCursor(Qt.CursorShape.ArrowCursor)
        self.spacer.setCursor(cursor)
        # self.spacer.setMinimumWidth(500)

        self.heading_layout.addWidget(self.btn_requery)
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
        
            
   

    def populate_form(self):
        values = self.list.get_values_dict()
        if values:
            self.form.populate(values)
        else:
            self.form.clear()

    def selectionChanged(self):
        self.save_record()

    def save_record(self):
        prev_id = self.form.save() 
        if prev_id:
            curr_id = self.list.get_id()
            self.requery()
            self.list.select_record_id(curr_id)
        else:
            self.populate_form()
       
    def delete_record(self):
        record_id = self.list.get_id()
        sql = '''
        --sql
        DELETE FROM registros WHERE id = ?;'''
        self.db.connect()
        self.db.cursor.execute(sql, (record_id,))
        self.db.connection.commit()
        self.db.connection.close()
        self.requery()

    def new_record(self):
        self.list.list.clearSelection()
        self.form.clear()
        self.form.date_.btnTodayPressed()
        self.form.title_.setFocus()

    # def open_folder(self):
    #     self.files_tree.folderOpen()

    def cancel_form_edit(self):
        if self.list.list.selectionModel().hasSelection():
            self.populate_form()
        else:
            self.form.clear()
        self.form.dirty = False
        

    

        
        

    


    
        






    






if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())