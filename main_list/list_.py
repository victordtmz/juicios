from PyQt6.QtWidgets import (QWidget, QVBoxLayout)
from widgets.treeviews import treeView

class main(QWidget):
    """main list of items that contains all the cases with their type.
    info is populated on parent widget requery() -> populate() functions. 
    Columns:
        0 => Heading: Tipo; data: case category. 
        1 => Heading: Expediente; data: Client name with short case explanation.
        2 => Heading: Activos; data: Actio or inactivo - for loading.

    Args:
        QWidget (_type_): _description_
    """
    def __init__(self):
        super().__init__()
        self.list = treeView()#params fontSize = 13, rowHeight = 42
        self.selection_model = self.list.selectionModel()
        self.list.standardModel.setHorizontalHeaderLabels(['Tipo', 'Expediente'])
        
        self.list.setColumnWidth(0, 140)

        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout_)
        # self.layout_.addWidget(self.activos_filter)
        # self.layout_.addWidget(self.btn_clear)
        self.layout_.addWidget(self.list,1)

    def add_item(self, item):
        """appends given item to end-bottom of the list

        Args:
            item (string): 
        """
        self.list.add_item(item)

    def remove_all_items(self):
        """Gets the total number of items to clear the list
        """
        self.list.remove_all_items()

    def get_values(self)->list:
        """Gets the values for the selected record

        Returns:
            list: list of string values selected
        """
        return self.list.get_values()

    def add_activos(self, items):
        """Adds record with font and row height defined on tree.

        Args:
            items (iterable): List of lists, tupple or set of iterable items (records)
        """
        self.list.add_items(items)

    def add_inactivos(self, items):
        """Adds items to list with a dark red color

        Args:
            items (iterable): List of lists, tupple or set of iterable items (records)
        """
        self.list.add_items(items, 'dark red')