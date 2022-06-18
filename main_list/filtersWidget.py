from PyQt6.QtWidgets import ( QWidget, QVBoxLayout)
from globalElements import constants
from globalElements.widgets.widgets import spacer, buttonWidget, labelWidget, titleBox, treeView, checkBox
from globalElements.widgets.lineEdits import lineEditFilterGroup


class main(QWidget):
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