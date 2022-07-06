import sys
from PyQt6.QtWidgets import (QGridLayout,QApplication, QHBoxLayout, QWidget, QStatusBar, QMainWindow)
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import Qt
from globalElements import constants
from widgets.widgets import yesNoWarningBox, buttonWidget, QMessageBox
from progreso import form, list_
from globalElements import db
from widgets.filesTree import filesTree
from globalElements.models import main


class main(main.main):
    """extends the QMainWindow Widget
    Contains list, form, and files folder for all notes, acuerdos and any general item for the juicios.

    Args:
        expediente (list): 
            0 => Tipo. ex('Administrativo', 'Civil', 'Tramites', etc...)
            1 => Name of folder where this file is stored. 
            2 => 'Juicios' or 'Juicios_archivados'
    """
    def __init__(self, expediente):
        super().__init__(expediente)
        
       
    def delete_record(self, id_): 
        """Deletes selected record from db, warning pop-up before delete.
        """
        self.db.delete_record_registros(id_)

        #Get the record as a dict, with the header values of the list
        # record = self.list.get_row_values_dict()
        # text = ''
        # #use the dict values to display the recods on the warning to delete
        # for k,v in record.items():
        #     text += f'{k}: {v} \n'

        # waring = yesNoWarningBox(text, 13)
        # delete_response = waring.exec()
        # #if warning response is yes, delete the record. 
        # if delete_response == QMessageBox.StandardButton.Yes:
        #     record_id = record['id']
        #     self.db.delete_record_registros(record_id)
        #     self.requery()
    def config_layout(self):
        """Configuration of the layout of all widets"""
        #init files window
        self.files_tree = filesTree()
        self.files_tree.setLineEditFileBox(13)
        self.files_tree.txtFilePath.setText(f'{self.folder}')
        
        #init Form
        self.db = db.juiciosDB()
        self.db.set_db(self.folder)
        self.form = form.main(self.folder)
        self.form.file_ = self.files_tree.layoutLineEditFileBox
        self.form.lineEditItems = self.files_tree.lineEditItems
        
        self.form.initiate_super()

        # init list
        self.list = list_.main(self.folder)

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

    def new_record(self):
        """Clears selection and form, sets todays date on form and focuses on title 
        - record will be saved unless operation is canceled)
        """
        self.list.list.clearSelection()
        self.form.clear()
        self.form.date_.btnTodayPressed()
        self.form.title_.setFocus()

    # def open_folder(self):
    #     self.files_tree.folderOpen()

    def cancel_form_edit(self):
        """If: list has selection, it will return the values to the list values
        else: it will clear the form and avoid saving the record unless data is imputed again. 
        """
        if self.list.list.selectionModel().hasSelection():
            self.populate_form()
        else:
            self.form.clear()
        self.form.dirty = False

    def before_closing(self):
        self.save_record()
        if hasattr(self.db, 'juiciosDB'):
            self.db.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = main()
    mw.show()
    sys.exit(app.exec())