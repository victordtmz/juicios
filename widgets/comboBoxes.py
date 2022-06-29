from typing import Iterable
from PyQt6.QtWidgets import QComboBox, QCompleter
from PyQt6.QtGui import QFont, QWheelEvent
from PyQt6.QtCore import Qt

class cbo(QComboBox):
    def __init__(self, 
            fontSize:int =13, 
            items:Iterable = [], 
            completionMode=QCompleter.CompletionMode.PopupCompletion):
        super().__init__()
        self.setEditable(True)
        font = QFont('Calibri', fontSize)
        self.setFont(font)
        
        self.sourceType = type(items)
        self.items = items
         
        if items:
            # if self.sourceType is dict:
            #     items = sorted(items, key = lambda i: i)
            # else:
            items = sorted(items)
            self.clear()
            self.addItems(items)
            self.completer_name = QCompleter(items)
            self.completer_name.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.completer_name.setCompletionMode(completionMode)
            self.setCompleter(self.completer_name) 
            
    def insertNewItems(self, items):
        self.clear()
        self.addItems(items)
        completer_name = QCompleter(items)
        completer_name.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        # completer_name.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        self.setCompleter(completer_name)

    def wheelEvent(self, e: QWheelEvent) -> None:
        e.ignore()

    def setConnection(self,e):
        self.currentTextChanged.connect(e)
    
    # def populate(self,text):    
    #     self.setCurrentText(text)

    def reSet(self):
        self.setCurrentIndex(0)

    def getInfo(self):
        return self.currentText()

    def populate(self,text):    
        if self.sourceType is dict:
            if text.isnumeric():
                for k, v in self.items.items():
                    if text == str(v):
                        text = k
                        break
        self.setCurrentText(text)

    def getDbInfo(self):
        currentText = self.currentText()
        if self.sourceType is list:
            text = currentText
        elif self.sourceType is dict:
            try: text = self.items[currentText]
            except KeyError: text = '' 
        else:
            text = self.sourceType
        return text