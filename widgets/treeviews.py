
import string
from globalElements import constants
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QSizePolicy,
    QComboBox, QCompleter, QHBoxLayout, QGroupBox, QGridLayout, QRadioButton,
    QDateEdit, QDateTimeEdit, QLineEdit, QMainWindow, QToolBar, QCheckBox,
    QMessageBox, QTabWidget, QTextEdit, QSpinBox, QTreeView)

from PyQt6.QtCore import (Qt, QSize, QDate, QDateTime)
from PyQt6.QtGui import (QWheelEvent, QFont, QIcon, QCursor, QGuiApplication,
    QTextDocument, QStandardItem, QColor, QBrush, QAction, QStandardItemModel)

class treeView(QTreeView):
    """inherits from QtreeView class
    Ordinary standard model tree with no filtering capabilities. 

        Args:
            fontSize (int, optional): font size to be used at all times for this tree. Defaults to 13.
            rowHeight (int, optional): row height to be used at all tmes for this tree. Defaults to 42.
        """
    def __init__(self, fontSize = 13, rowHeight = 42):
        
        super().__init__()
        self._fontSize = fontSize
        self._rowHeight = rowHeight
        self.standardModel = QStandardItemModel()
        self.rootNode = self.standardModel.invisibleRootItem()
        
        self.setModel(self.standardModel)
        self.setRootIsDecorated(False)

    

    def add_item(self, record, color_var ='#000000',  weight = 400):
        """Converts record provided to standardItem and appends a new row. 

        Args:
            record (iterable): list of strings. 
            colorVar (str, optional): css hex or color value for text . Defaults to '#000000'.
            weight (int, optional): font weight. Defaults to 400.
        """
        record = list(map(lambda text: 
            standardItem(text, self._fontSize, self._rowHeight, color_var, weight),
            record))
        self.rootNode.appendRow(record)

    def add_items(self, records, color_var ='#000000',  weight = 400):
        """For record in records, call add_item.  Appends all records to the list.

        Args:
            records (iterable): a list of lists to be addes ad records. 
            colorVar (str, optional): css hex or color value for text . Defaults to '#000000'.
            weight (int, optional): font weight. Defaults to 400.
        """
        for i in records:
            self.add_item(i, color_var, weight)

    def remove_all_items(self):
        self.standardModel.removeRows(0, self.standardModel.rowCount())
    
    def get_row_values(self)-> list:
        """Returns:
            list: returns of list of values for the selected record
        """
        indexes = self.selectionModel().selectedIndexes()
        values = list(map(lambda i: i.data(), indexes))
        return values

    def get_row_values_dict(self)->dict:
        """
        Returns:
            dict: Dictionary with row values with headers as keys
        """
        indexes = self.selectionModel().selectedIndexes()
        values = list(map(lambda i: i.data(), indexes))
        dict_values = {}
        index = 0
        for value in values:
            column_header = self.standardModel.horizontalHeaderItem(index)
            if column_header:
                header_text = column_header.text()
                dict_values[header_text] = value
            index += 1
        return dict_values

       

        
class standardItem(QStandardItem):
    """Standard item to be used with treeview widget - to place string elements to constitute a record

        Args:
            txt (str, optional): String to be placed ->data(). Defaults to ''.
            fontSize (int, optional): Font size. Defaults to 13.
            rowHeight (int, optional): Row height. Defaults to 42.
            colorVar (str, optional): font color. Defaults to '#000000'.
            weight (int, optional): font weight. Defaults to 400.
        """
    def __init__(self,  txt='',fontSize = 13, rowHeight=42, colorVar ='#000000', weight = 400):
        
        super().__init__()
        self.font_ = QFont('Calibri', fontSize, weight)
        self.setFont(self.font_)
        self.setText(str(txt))
        self.setForeground(QColor(colorVar))
        self.setSizeHint(QSize(20,rowHeight))
        self.setEditable(True)
    
    def __repr__(self) -> str:
        return f'standarditem => {self.text()}'

