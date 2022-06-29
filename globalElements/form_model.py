from abc import abstractmethod
from PyQt6.QtWidgets import QWidget, QFormLayout, QScrollArea, QSizePolicy, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from widgets.lineEdits import (lineEdit, 
    lineEditCurrency, dateWidget, lineEditPhone)
from widgets.widgets import textEdit, buttonWidget, labelWidget
from globalElements import constants

class main(QScrollArea):
    def __init__(self):
        super().__init__()
        self.fontSize = 13
        self.dirty = False
        self.init_model_ui()
        
    def init_model_ui(self):
        self.setWidgetResizable(True)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.configure_layout()
        self.configureForm()
        self.set_main_connections()

    def configure_layout(self):
        #title layout
        self.title = labelWidget('Formulario', 18, True, 'white', 'center', '#002142', '5px')

        #form items layout
        self.form_widget = QWidget()
        self.form_widget.setMinimumWidth(600)
        self.form_layout = QFormLayout()
        self.form_widget.setLayout(self.form_layout)

        #save and cancel buttons
        self.btn_widget = QWidget()
        self.btn_layout = QHBoxLayout()
        self.btn_widget.setLayout(self.btn_layout)
        self.btn_save = buttonWidget('Guardar', 13, constants.iconSave, 'h2')
        self.btn_cancel = buttonWidget('Cancelar', 13, constants.iconCancel, 'h2')
        self.btn_layout.addWidget(self.btn_cancel)
        self.btn_layout.addWidget(self.btn_save)

        #main layout
        self.widget_ = QWidget()
        self.setWidget(self.widget_)
        self.layout_ = QVBoxLayout()
        self.widget_.setLayout(self.layout_)
        self.layout_.addWidget(self.title)
        self.layout_.addWidget(self.form_widget)
        self.layout_.setAlignment(self.form_widget, Qt.AlignmentFlag.AlignHCenter)
        self.layout_.addWidget(self.btn_widget)

    @abstractmethod
    def configureForm(self):
        self.formItems = {}

        

        
    
    

    def clear(self):
        for i in self.formItems.values():
            i.reSet()

    def populate(self, content):
        index = 0
        for i in self.formItems.values():
            i.populate(content[index])
            index += 1

    # def form_values_populate(self):
    #     for i in self.formItems:
    #         self.formValues.append(i.getDbInfo())

    def get_info(self):
        return list(map(lambda x: x.getDbInfo(), self.formItems.values()))

    def set_main_connections(self):
        for i in self.formItems.values():
            i.editingFinished.connect(self.set_form_dirty)
    
    def set_form_dirty(self):
        self.dirty = True
