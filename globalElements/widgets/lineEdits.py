from globalElements.functions import formatPhoneNo
from globalElements import constants
from globalElements.widgets import widgets
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QLineEdit, QDateEdit)
# from PyQt6.QtCore import (Qt, QSize, QDate, QDateTime)
from PyQt6.QtGui import (QFont, QWheelEvent)
from PyQt6.QtCore import QDate
import locale
locale.setlocale(locale.LC_ALL,"")
import re
from datetime import datetime
from globalElements.widgets.widgets import buttonWidget

class lineEdit(QLineEdit):
    """lineEdit
        inherits => QLineEdit

        Args:
            fontSize (int, optional): Item font Size. Defaults to 13.
            hightLight (bool, optional): if set to true, item background will be colored. Defaults to False.
        """
    def __init__(self, fontSize = 13, hightLight=False):
        super().__init__()
        font = QFont('Calibri', fontSize)
        self.setFont(font)
        if hightLight:
            self.setStyleSheet("QLineEdit"
                        "{"
                        "background : #ffeeda;"
                        "}")

    def populate(self, text):
        """set te value to the given string

        Args:
            text (string): text to populate
        """
        self.setText(text)
    
    def reSet(self):
        """sets the current value to ""
        """
        self.clear()

    def getInfo(self) -> str:
        """
        Returns:
            string: item text
        """
        return self.text()

    def __repr__(self) -> str:
        return f'QLineEdit [text] => {self.text()}'


class lineEditFilterGroup(QWidget):
    """A widget containing horizontally 3 widgets (2 optional):
    label => a string value for label param must be given to include in layout. 
    lineEdit => Ordinary lineEdit widget.
    button => Clear filter button, removes lineEdit content and sets focus to it on pressed.

        Args:
            fontSize (int, optional): lineEdit font size. Defaults to 13.
            label (str, optional): if a label is set, it will be included in the HBoxLayout. Defaults to "".
            clearFilter (bool, optional): if True, a button will be added at the end to clear the text. Defaults to True.
        """
    def __init__(self, fontSize =13, label = "", clearFilter = True):
        
        super().__init__()
        self.txt = lineEdit(fontSize)
        self.btn = widgets.buttonWidget(icon=constants.iconClearFilter)
        self.btn.setFixedSize(30, fontSize * 2)
        self.layout_ = QHBoxLayout()
        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0,0,0,0)
        self.layout_.addWidget(self.txt,1)
        
        if clearFilter:
            self.layout_.addWidget(self.btn)
        
        self.setLayout(self.layout_)
        if label:
            self.lbl = widgets.labelWidget(label,fontSize)
            self.layout_.insertWidget(0, self.lbl)

        self.btn.pressed.connect(self.btn_pressed)
    
    def btn_pressed(self):
        """Clears line edit content and sets focus to it
        """
        self.txt.clear()
        self.txt.setFocus()

    def populate(self,text):   
        """Populates txt widget. 
        Args:
            text (string): text used to populate lineEdit.
        """ 
        self.txt.populate(text)

    def reSet(self):
        """Sets the value of txt to ""
        """
        self.txt.reSet()

    def getInfo(self):
        """Returns:
            string: content of 'txt' widget"""
        return self.txt.text()

    def currentText(self):
        """Returns:
            string: content of 'txt' widget"""
        return self.getInfo()

    def __repr__(self) -> str:
        return 'label, lineEdit, button => filter Group'

class lineEditPhone(lineEdit):
    def __init__(self, fontSize =13):
        super().__init__(fontSize)
        self.firstPass = ''
        self.textChanged.connect(self.format)
        
    
    def getInfo(self):
        currentNo = ''.join(re.findall(r'\d',self.text()))
        return currentNo
        

    def format(self):
        inputValue = self.text()
        inputLength = len(inputValue)
        if inputLength > 3:
            #only evauate if more than 3 elements. 
            currentNo = ''.join(re.findall(r'\d',inputValue))
            currentNoLength = len(currentNo)
            # only format if more than 3 digits
            if currentNoLength > 3:
                try:
                    formatedNo = '(%s) %s-%s' % tuple(re.findall(r'\d{4}$|\d{3}',str(currentNo)))
                    if not formatedNo == inputValue:
                        self.changeValue(currentNo)
                except:
                    self.changeValue(currentNo)
            

    def changeValue(self,currentNo):
        PhoneNo = formatPhoneNo(currentNo)
        self.setText(PhoneNo)
class lineEditCurrency(lineEdit):
    def __init__(self, fontSize):
        super().__init__(fontSize)
    
    def getInfo(self):
        return self.text()
    
    def getDbInfo(self):
        info = self.text()
        if info:
            try:
                info = locale.atof(str(info).strip("$()"))
                return str(info)
            except:
                return ""
            # print(info)
            
    def populate(self, text):
        if text:
            text = str(text).strip("()")
            if "$" in text:
                self.setText(text)
            else:
                amount = float(text)
                amount = locale.currency(amount, grouping=True)
                self.setText(amount)

    
    def reSet(self):
        self.clear()

class dateEdit(QDateEdit):
    def __init__(self, fontSize = 13):
        super().__init__()
        self.setCalendarPopup(True)
        self.setDisplayFormat('yyyy-MM-dd')
        # self.setDate(QDate.currentDate())
        font = QFont('Calibri', fontSize)
        self.setFont(font)
    
    def wheelEvent(self, e: QWheelEvent) -> None:
        e.ignore()

    def populate(self, text):
        try:
            fecha = datetime.strptime(text, '%Y-%m-%d')
        except:
            fecha = datetime(2000,1,1)
        self.setDate(fecha)

    def reSet(self):
        fecha = datetime(2000,1,1)
        self.setDate(fecha)

    def getInfo(self):
        return self.text()

class dateWidget(QWidget):
    def __init__(self, fontSize = 13):
        super().__init__()
        self.dateEdit = dateEdit(fontSize) 
        self.btnToday = buttonWidget(icon=constants.iconToday)
        self.btnToday.setMinimumHeight(30)

        self.layout_ = QHBoxLayout()
        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0,0,0,0)
        # self.layout_.addWidget(self.lbl)
        self.layout_.addWidget(self.dateEdit,1)
        self.layout_.addWidget(self.btnToday)
        self.setLayout(self.layout_)

        self.btnToday.pressed.connect(self.btnTodayPressed)
        
    def btnTodayPressed(self):
        self.dateEdit.setDate(QDate.currentDate())

    def populate(self, text):
        self.dateEdit.populate(text)
        
    def reSet(self):
        self.dateEdit.reSet()

    def getInfo(self):
        return self.dateEdit.getInfo()