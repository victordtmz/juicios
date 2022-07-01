
from abc import abstractmethod
import string
from tkinter.ttk import Style
from globalElements import constants
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QSizePolicy,
    QComboBox, QCompleter, QHBoxLayout, QGroupBox, QGridLayout, QRadioButton, QVBoxLayout,
    QDateEdit, QDateTimeEdit, QLineEdit, QMainWindow, QToolBar, QCheckBox,
    QMessageBox, QTabWidget, QTextEdit, QSpinBox, QTreeView)

from PyQt6.QtCore import (Qt, QSize, QDate, QDateTime, pyqtSignal)
from PyQt6.QtGui import (QWheelEvent, QFont, QIcon, QCursor, QGuiApplication,
    QTextDocument, QStandardItem, QColor, QBrush, QAction, QStandardItemModel, QFocusEvent)

class widget_model(QWidget):
    editingFinished = pyqtSignal()
    def __init__(self, fontSize=11):
        super(widget_model, self).__init__()
        self._fontSize = fontSize
        self.font_ = QFont('Calibri', fontSize)
        self.init_widget()

    @abstractmethod
    def create_main_widget(self):
        self.main_widget = textEdit()

    def init_widget(self):
        self.create_main_widget()
        self.configure_main_widget()
        self.main_widget.editingFinished.connect(self.editingFinished_)
        self.editingFinished.connect(self.execute_validation)

        self.layout_ = QVBoxLayout()
        self.setLayout(self.layout_)
        self.layout_.setContentsMargins(0,0,0,0)
        self.layout_.addWidget(self.main_widget)

    def configure_main_widget(self):
        self.main_widget.setFont(self.font_)

    def set_validation(self, text:str=''):
        if hasattr(self, 'validation_label'):
            self.validation_label.deleteLater()
            del self.validation_label
            # self.deletea
        if text:
            self.validation_label = labelWidget(text,self._fontSize-1, fontColor='red')
            self.layout_.insertWidget(0, self.validation_label)
            self.main_widget.setFocus()

    # @abstractmethod
    # def execute_validation(self, text): 
    #     self.set_validation(text)



    def populate(self, text):
        self.main_widget.populate(text)
    
    def reSet(self):
        self.main_widget.reSet()

    def getInfo(self):
        return self.main_widget.getInfo()
    
    def getDbInfo(self):
        return self.main_widget.getDbInfo()

    def __repr__(self) -> str:
        return 'Widgeg model - Contains validation methods and label'
    
    def editingFinished_(self):
        self.editingFinished.emit()

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
    
    def get_values(self)-> list:
        """Returns:
            list: returns of list of values for the selected record
        """
        indexes = self.selectionModel().selectedIndexes()
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
    def __init__(self, text:str="", fontSize:int=0, icon:str="", size:str='h1'):
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

        match size.lower():
            case 'h1':
                self.setMinimumHeight(32)
                style = '''
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
                    '''
            case 'h2':
                self.setMinimumHeight(28)
                style = '''
                    QPushButton {
                        background-color: #003D7A;
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
                    '''

            case 'h2_form':
                self.setMinimumHeight(28)
                style = '''
                    QPushButton {
                        background-color: #134A4D;
                        
                        color :white  ;
                        border-radius: 5px;
                        padding-right: 15px;
                        padding-left: 15px;
                        
                        
                        border-width: 1px;
                        }
                    QPushButton:pressed {
                        background-color: rgba(0,51,0,.2);
                        border-color: rgba(0,51,0,1);
                        color : Black ;
                        
                        border-radius: 5px;
                        border-width: 1px;
                        }
                        
                    QPushButton:hover:!pressed { 
                        background-color: rgba(0,51,0,.6);
                        border-color: rgba(0,51,0,1);
                        }
                    '''

            case 'icon':
                self.setFixedSize(28,28)
                # style = '''
                #     QPushButton {
                #         background-color: #dce5fc;
                #         color :white  ;
                #         padding-right: 15px;
                #         padding-left: 15px;
                #         margin: 0;
                #         border-style: solid;
                #         border-width: 1px;
                #         border-color: #b5b5b5;
                #         }
                    
                #     QPushButton:pressed {
                #         background-color: rgba(0,51,0,.2);
                #         color : Black ;
                #         }

                #     QPushButton:hover:!pressed { 
                #         text-decoration: underline;
                #         background-color: #a7bffc;
                #         }
                #     '''

        if 'style' in locals():
            self.setStyleSheet(style)

        

        
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

    def __repr__(self) -> str:
        return f'labelWidget => {self.text()}'

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

class textEdit(QTextEdit):
    editingFinished = pyqtSignal()
    
    def __init__(self, fontSize=11):
        super(textEdit, self).__init__()
        font = QFont('Calibri', fontSize)
        self.setFont(font)
        self.setMinimumHeight(170)
        # self.dirty = False
        self.on_focus_content = ''
        # self.editingFinished.connect(self.testSignal)
        self.textChanged.connect(self.textChanged_)

    def populate(self, text):
        self.setText(text)
        # self.dirty = False
    
    def reSet(self):
        self.clear()

    def getInfo(self):
        return self.toPlainText()
    
    def getDbInfo(self):
        return self.getInfo()

    def __repr__(self) -> str:
        return 'textEdit - Large text widget'

    def focusInEvent(self, e: QFocusEvent) -> None:
        self.on_focus_content = self.getInfo()
        return super().focusInEvent(e)

    def focusOutEvent(self, e: QFocusEvent) -> None:
        on_focus_out_content = self.getInfo()
        if self.on_focus_content != on_focus_out_content:
            self.editingFinished.emit()
        return super().focusOutEvent(e)
    
    def textChanged_(self):
        self.dirty = True
    
class okWarningBox(QMessageBox): 
    def __init__(self, text='', fontSize=13):
        super().__init__()
        self.iconAVD = QIcon( f'{constants.ICONS_FOLDER}\enlace.png')
        self.setWindowTitle('Eliminar registro')
        self.setWindowIcon(QIcon(f'{constants.ICONS_FOLDER}\enlace.png'))
        self.setText(text)
        # self.setStyleSheet("QLabel{min-width: 200px;}")
        # self.setInformativeText('Continue?')
        font = QFont('Calibri', fontSize)
        self.setFont(font)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setIcon(QMessageBox.Icon.Information)

class yesNoWarningBox(okWarningBox): 
    def __init__(self, text='', fontSize=13):
        super().__init__(text, fontSize)
        self.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)


class tabWidget(QTabWidget):
    tab_closed = pyqtSignal()
    def __init__(self, size:str="h1"):#self, fontSize=10, selectedSize=16
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.setTabsClosable(True)
        self.setMinimumHeight(170)
        self.setTabBarAutoHide(True)
        
        #style
        

        match size.lower():
            case 'h1':
                css = """
                QTabBar:tab {
                    background-color:rgb(212, 212, 212);
                    color: #002142;
                    font-size: 12px;
                    border-radius: 1px;
                    
                    padding-top: 2px;
                    padding-right: 20px;
                    padding-left: 20px;
                    padding-bottom: 2px;
                    }
                QTabBar:tab:selected {
                    background-color:#002142;
                    color: rgb(212,212,212);
                    font-size: 14px;
                    padding-top: 2px;
                    padding-right: 20px;
                    padding-left: 20px;
                    padding-bottom: 2px;
                    }
                """
            case 'h2':
                css = """
                QTabBar:tab {
                    background-color:rgb(212, 212, 212);
                    color: #134A4D;
                    
                    font-size: 12px;
                    border-radius: 1px;
                    
                    padding-top: 2px;
                    padding-right: 20px;
                    padding-left: 20px;
                    padding-bottom: 2px;
                    }
                QTabBar:tab:selected {
                    
                    background-color:#134A4D;
                    color:rgb(212, 212, 212);
                    font-size: 14px;
                    padding-top: 2px;
                    padding-right: 20px;
                    padding-left: 20px;
                    padding-bottom: 2px;
                    }
                """

        
        self.setStyleSheet(css)

        self.tabCloseRequested.connect(self.close_tab_requested)
    
    

    def close_tab_requested(self, index):
        self.tab_closed.emit()
        if index:
            self.removeTab(index)