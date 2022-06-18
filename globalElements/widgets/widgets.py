
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
    def __init__(self, fontSize = 13, rowHeight = 42):
        super().__init__()
        self._fontSize = fontSize
        self._rowHeight = rowHeight
        self.standardModel = QStandardItemModel()
        self.rootNode = self.standardModel.invisibleRootItem()
        
        self.setModel(self.standardModel)
        self.selection_model = self.selectionModel()
        self.setRootIsDecorated(False)

    

    def add_item(self, record, color_var ='#000000',  weight = 400):
        """Converts record provided to standardItem and appends a new row. 

        Args:
            record (iterable): list of strings. 
            colorVar (str, optional): css hex or color value for text . Defaults to '#000000'.
            weight (int, optional): font weight. Defaults to 400.
        """
        # if not isinstance(record, str):
        record = list(map(lambda text: 
            standardItem(text, self._fontSize, self._rowHeight, color_var, weight),
            record))
        # else:
        #     record = standardItem(record, self._fontSize, self._rowHeight)
        self.rootNode.appendRow(record)

    def add_items(self, records, color_var ='#000000',  weight = 400):
        """For record in records, call add_item.  Appends all records to the list.

        Args:
            records (iterable): a list of lists to be addes ad records. 
            colorVar (str, optional): css hex or color value for text . Defaults to '#000000'.
            weight (int, optional): font weight. Defaults to 400.
        """
        # map(lambda r: self.add_item(r, color_var, weight), records)
        for i in records:
            self.add_item(i, color_var, weight)

    def remove_all_items(self):
        self.standardModel.removeRows(0, self.standardModel.rowCount())
    
    def get_values(self)-> list:
        """Returns:
            list: returns of list of values for the selected record
        """
        indexes = self.selection_model.selectedIndexes()
        values = list(map(lambda i: i.data(), indexes))
        return values

class spacer(QLabel):
    def __init__(self, text='', size="h1"):
        super().__init__(text)
        
        if size.lower() == "h1".lower():
            self.setStyleSheet('''
            QWidget {
                background-color:#002142;
                }
            ''')
        else:
            self.setStyleSheet('''
            QWidget {background-color:#134A4D}
            ''')

class titleBox(QWidget):
    def __init__(self, size="h1"):
        super().__init__()
        self.setMinimumHeight(30)
        self.setStyleSheet('''
            QWidget {
                background-color:#002142;
                }
            ''')
        

        self.layout_ = QHBoxLayout()
        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout_)



class buttonWidget(QPushButton):
    def __init__(self, text="", fontSize=0, icon=""):
        super().__init__()
        cursor = QCursor(Qt.CursorShape.PointingHandCursor)
        self.setCursor(cursor)
        font = QFont('Calibri', 11)
        
        if icon:
            icon = QIcon(icon)
            self.setIcon(icon)
        if text:
            self.setText(text)
        if fontSize:
            font.setPointSize(fontSize)

        self.setFont(font)
        # self.setMinimumHeight(35)

        self.setStyleSheet('''
            QPushButton {
                background-color: #002142;
                color :white  ;
                padding-right: 15px;
                padding-left: 15px;
                margin: 0;
                border-style: none;
                }
            
            QPushButton:pressed {
                background-color: rgba(0,51,0,.2);
                color : Black ;
                }

            QPushButton:hover:!pressed { 
                text-decoration: underline;
                }
        ''')

        

        
class standardItem(QStandardItem):
    def __init__(self,  txt='',fontSize = 13, rowHeight=42, colorVar ='#000000', weight = 400):
        super().__init__()
        self.font_ = QFont('Calibri', fontSize, weight)
        self.setFont(self.font_)
        self.setText(str(txt))
        self.setForeground(QColor(colorVar))
        self.setSizeHint(QSize(20,rowHeight))
        self.setEditable(False)
    
    def __repr__(self) -> str:
        return f'standarditem => {self.text()}'

class actionBtn(QAction):
    def __init__(self, text = '', fontSize = 0, icon = ''):
        super().__init__()
        font = QFont('Calibri', 11)
        if fontSize:
            font.setPointSize(fontSize)
            self.setFont(font)

        if icon:
            self.setIcon(QIcon(icon))

        if text:
            self.setText(text)
            # self.setToolTip(text)
            self.setStatusTip(text)

class btnToolBar(QPushButton):
    def __init__(self, text = '', fontSize = 0, icon = ''):
        super().__init__()
        font = QFont('Calibri', 11)
        if fontSize:
            font.setPointSize(fontSize)
            self.setFont(font)

        if icon:
            self.setIcon(QIcon(icon))

        if text:
            self.setText(text)
            # self.setToolTip(text)
            self.setStatusTip(text)

class labelWidget(QLabel):
    def __init__(self, text="", fontSize=0, fontBolt = False, fontColor = "" , align = "", backColor = "", padding="0px" ): 
        super().__init__() 
        
        font = QFont('Calibri', 11)
        self.setText(text)
        
        if fontSize:
            font.setPointSize(fontSize)
        
        if fontBolt:
            font.setBold(True)
            
        self.setFont(font)
        

        if fontColor and backColor:
            self.setStyleSheet('''
                QLabel {
                color:%s;
                background-color:%s;
                padding: %s;
                };''' % (fontColor, backColor, padding))
        
        elif fontColor and not backColor:
            self.setStyleSheet('''
                QLabel {
                color:%s;
                padding: %s;
                };''' % (fontColor, padding))
        
        elif not fontColor and backColor:
            self.setStyleSheet('''
                QLabel {
                background-color:%s;
                padding: %s;
                };''' % (backColor, padding))

        if align:
            if align == "center":
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)
            elif align == "right":
                self.setAlignment(Qt.AlignmentFlag.AlignRight)

class checkBox(QCheckBox):
    def __init__(self, text='', fontSize = 0, size=''):
        super().__init__()
        cursor = QCursor(Qt.CursorShape.PointingHandCursor)
        self.setCursor(cursor)
        font = QFont('Calibri', 11)
        if text:
            if fontSize:
                font.setPointSize(fontSize)
            self.setFont(font)
            self.setText(text)
        if size == 'h1' or size == 'h2':
            self.setStyleSheet('QCheckBox {color: white} ')
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        

    
    def populate(self, value):
        if value == '1' or value.lower() == "true":
            self.setChecked(True)
        else:
            self.setChecked(False)
    
    def reSet(self):
        self.setChecked(False)

    def getInfo(self):
        if self.isChecked():
            return 'True'
        else:
            return 'False'

    def getDbInfo(self):
        if self.isChecked():
            return "1"
        else:
            return "0"

